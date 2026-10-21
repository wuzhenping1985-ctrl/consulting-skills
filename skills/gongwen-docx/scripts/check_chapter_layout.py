"""Check chapter starts and one-body-line spacing before section headings."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from docx import Document
from docx.oxml.ns import qn

SERIAL = r'第[一二三四五六七八九十百千万零〇0-9]+'


def paragraph_property(paragraph, tag, attr='val', default=None):
    # Direct formatting takes priority; then follow the paragraph style chain.
    containers = [paragraph._p.pPr]
    style = paragraph.style
    seen = set()
    while style is not None and style.style_id not in seen:
        seen.add(style.style_id)
        containers.append(style.element.pPr)
        style = style.base_style
    for container in containers:
        element = None if container is None else container.find(qn('w:' + tag))
        if element is not None:
            value = element.get(qn('w:' + attr))
            if value is not None:
                return value
            if attr == 'val' and tag != 'spacing':
                return '1'
    return default


def check(path, body_line_pt=None):
    document = Document(path)
    lines = Counter()
    for paragraph in document.paragraphs:
        if not paragraph.text.strip():
            continue
        if paragraph.style.name in ('Caption', 'GovNote', 'GovSource', 'GovLegend', 'GovAxis', 'Footnote Text', 'Endnote Text'):
            continue
        if paragraph_property(paragraph, 'outlineLvl', default='9') == '9':
            if paragraph_property(paragraph, 'spacing', 'lineRule') == 'exact':
                line = paragraph_property(paragraph, 'spacing', 'line')
                if line:
                    lines[int(line)] += 1
    line_twips = round(body_line_pt * 20) if body_line_pt is not None else (lines.most_common(1)[0][0] if lines else None)
    errors, chapters, sections = [], [], []
    if line_twips is None:
        errors.append('未识别固定正文行距，请使用--body-line-pt明确指定')
    previous = None
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        if not text:
            continue
        is_heading = int(paragraph_property(paragraph, 'outlineLvl', default='9')) < 9 or paragraph.style.name.startswith('Heading ')
        chapter = is_heading and re.match(r'^' + SERIAL + r'章(?:\s|\S)', text)
        section = is_heading and re.match(r'^' + SERIAL + r'节(?:\s|\S)', text)
        if chapter or section:
            label = f'段落{index} {text}'
            if paragraph_property(paragraph, 'jc', default='left') != 'center':
                errors.append(f'{label}：章、节标题须居中对齐')
            for tag in ('keepNext', 'keepLines'):
                if paragraph_property(paragraph, tag, default='0') not in ('1', 'true', 'on'):
                    errors.append(f'{label}：{tag}未开启')
        if chapter:
            chapters.append({'paragraph': index, 'title': text})
            if paragraph_property(paragraph, 'pageBreakBefore', default='0') not in ('1', 'true', 'on'):
                errors.append(f'{label}：未设置段前分页')
            if int(paragraph_property(paragraph, 'spacing', 'before', '0')) != 0:
                errors.append(f'{label}：章首页额外设置段前空白')
        if section:
            before = int(paragraph_property(paragraph, 'spacing', 'before', '0'))
            prior_after = int(paragraph_property(previous, 'spacing', 'after', '0')) if previous is not None else 0
            sections.append({'paragraph': index, 'title': text, 'before_twips': before, 'previous_after_twips': prior_after})
            # Word normally collapses adjacent paragraph spacing to its maximum.
            # A preceding chart note may already supply the one-line gap.
            effective_gap = max(before, prior_after)
            if line_twips is not None and effective_gap != line_twips:
                errors.append(f'{label}：相邻段落间距{effective_gap} twips，应为正文一行{line_twips} twips')
            if line_twips is not None and prior_after > line_twips:
                errors.append(f'{label}：前段段后间距超过一个正文行，须核查重复累计')
        previous = paragraph
    return {'path': str(Path(path).resolve()), 'scope': 'chapter_section_layout', 'body_line_twips': line_twips, 'chapters': chapters, 'sections': sections, 'passed': not errors, 'errors': errors, 'render_review_required': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('docx')
    parser.add_argument('--body-line-pt', type=float)
    parser.add_argument('--output-json')
    args = parser.parse_args()
    report = check(args.docx, args.body_line_pt)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(output)
    print(output)
    raise SystemExit(0 if report['passed'] else 1)
