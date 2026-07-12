---
name: gov-doc-format-cn
description: Convert, reformat, or typeset Chinese official party/government documents from Word or PDF input into a DOCX that follows the Party and Government Organs Official Document Format (GB/T 9704-2012) and related Chinese official-document handling rules. Use when the user provides or mentions a .docx/.doc/.pdf file and asks for 党政公文格式、公文规范排版、红头文件格式、政府公文 Word 输出、or strict official-document layout.
---

# Gov Doc Format Cn

## Workflow

1. Identify the input file and target output path. Prefer `.docx`; for `.doc`, convert to `.docx` first with Word/LibreOffice if available.
2. If accuracy matters, read `references/format-checklist.md` before editing or reviewing output.
3. Run `scripts/format_gov_doc.py` for deterministic layout:

```powershell
python .\scripts\format_gov_doc.py -i input.docx -o output.docx
python .\scripts\format_gov_doc.py -i input.pdf -o output.docx --title "关于进一步规范工作的通知"
```

4. Open or render-check the output DOCX when possible. Confirm page size, margins, title, body text, headings, attachments, signature/date, and page numbers.
5. Tell the user where the formatted DOCX was saved and note any extraction limits, especially for scanned PDFs or legacy `.doc` files.

## Formatting Rules

Apply the current standard baseline:

- A4 paper; margins: top 37 mm, bottom 35 mm, left 28 mm, right 26 mm.
- Main title: centered, 2号, 小标宋体 when available; use SimSun fallback if the font is unavailable.
- Insert one blank line after the main title before正文 begins.
- Main body: 3号, 仿宋_GB2312 when available; line spacing fixed at 28 pt; first-line indent 2 Chinese characters.
- Remove unnecessary spaces inside Chinese text, especially accidental spaces between Chinese characters, digits, and Chinese punctuation. Preserve necessary spaces, including the single customary space after chapter-style heading markers like `第一节 XXX` and spaces inside English phrases.
- Chapter-style subheadings named with `篇`, `章`, or `节`, such as `第一章 总则`, must be centered with one blank line above and one blank line below.
- Non-centered subheadings must start with a first-line indent of 2 Chinese characters.
- First-level headings like `一、`: 3号黑体.
- Second-level headings like `（一）`: 3号楷体_GB2312.
- Third-level headings like `1.` or `1．`: 3号仿宋_GB2312, bold.
- Attachments and signature/date blocks: keep official-document conventions; align signature/date to the right when detected.
- Page numbers: Arabic numerals in the footer with short dash marks, 4号宋体.

## PDF Handling

Use the script for text-based PDFs. If the PDF is scanned or extraction is garbled, use OCR first, then run the extracted DOCX/text through this skill. Do not silently invent missing content; preserve extracted text and flag uncertain areas.

## Quality Bar

Treat this as typesetting, not rewriting. Preserve the original wording unless the user explicitly asks for polishing. If required elements are absent (发文字号、主送机关、附件、成文日期等), format what exists and mention the missing items rather than fabricating them.
