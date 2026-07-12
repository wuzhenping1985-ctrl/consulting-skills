#!/usr/bin/env python3
"""Audit PPTX files for common PDF-to-editable-PPT requirements.

Checks:
- shadow effect tags in slide XML
- font typefaces that are not Microsoft YaHei / Microsoft YaHei theme fonts / approved KPI display fonts
- visible NotebookLM watermark/footer text
- text runs below 10pt and below 12pt
- text-containing shapes missing a 0.1 cm left inset
- text-containing shapes without explicit automatic text wrapping
- table cells missing a 0.1 cm left margin
- possible overlap between text-containing objects

The audit is intentionally conservative. Review warnings manually.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

TARGET_INSET_EMU = 36000
INSET_TOLERANCE_EMU = 1000
ALLOWED_FONTS = {"Microsoft YaHei", "微软雅黑", "Impact", "Arial"}
SHADOW_RE = re.compile(r"(?:^|})\w*shdw$", re.IGNORECASE)
WATERMARK_RE = re.compile(r"notebook\s*lm", re.IGNORECASE)
MIN_FONT_HARD = 1000
MIN_FONT_REVIEW = 1200
MIN_OVERLAP_AREA_EMU2 = 50_000_000
MIN_OVERLAP_RATIO = 0.08


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_xml(data: bytes, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(data)
    except ET.ParseError:
        return None


def attr_int(element: ET.Element, attr: str) -> int | None:
    value = element.get(attr)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def near_target(value: int | None) -> bool:
    return value is not None and abs(value - TARGET_INSET_EMU) <= INSET_TOLERANCE_EMU


def shape_name(shape: ET.Element) -> str:
    c_nv_pr = shape.find(".//p:cNvPr", NS)
    if c_nv_pr is not None:
        return c_nv_pr.get("name") or c_nv_pr.get("id") or "unknown"
    return "unknown"


def element_text(element: ET.Element) -> str:
    return "".join(t.text or "" for t in element.findall(".//a:t", NS))


def object_name(element: ET.Element) -> str:
    c_nv_pr = element.find(".//p:cNvPr", NS)
    if c_nv_pr is not None:
        return c_nv_pr.get("name") or c_nv_pr.get("id") or "unknown"
    return "unknown"


def object_bbox(element: ET.Element) -> tuple[int, int, int, int] | None:
    xfrm = element.find("./p:spPr/a:xfrm", NS)
    if xfrm is None:
        xfrm = element.find("./p:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("./a:off", NS)
    ext = xfrm.find("./a:ext", NS)
    if off is None or ext is None:
        return None
    x = attr_int(off, "x")
    y = attr_int(off, "y")
    cx = attr_int(ext, "cx")
    cy = attr_int(ext, "cy")
    if None in (x, y, cx, cy) or cx <= 0 or cy <= 0:
        return None
    return (x, y, x + cx, y + cy)


def rect_area(rect: tuple[int, int, int, int]) -> int:
    return max(0, rect[2] - rect[0]) * max(0, rect[3] - rect[1])


def intersection_area(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def text_object_candidates(root: ET.Element) -> list[dict]:
    candidates = []
    for element in root.findall(".//p:sp", NS) + root.findall(".//p:graphicFrame", NS):
        text = element_text(element).strip()
        if not text:
            continue
        bbox = object_bbox(element)
        if bbox is None:
            continue
        candidates.append(
            {
                "name": object_name(element),
                "text_sample": text[:40],
                "bbox": bbox,
                "area": rect_area(bbox),
            }
        )
    return candidates


def slide_sort_key(name: str) -> tuple[int, str]:
    match = re.search(r"slide(\d+)\.xml$", name)
    if match:
        return (int(match.group(1)), name)
    return (sys.maxsize, name)


def audit_slide(xml: bytes, slide_name: str) -> dict:
    root = parse_xml(xml, slide_name)
    result = {
        "slide": slide_name,
        "shadows": [],
        "fonts": [],
        "watermark_text": [],
        "font_sizes_below_10pt": [],
        "font_sizes_below_12pt": [],
        "shape_insets": [],
        "shape_wrap_warnings": [],
        "table_cell_margins": [],
        "possible_text_overlaps": [],
    }
    if root is None:
        result["parse_error"] = True
        return result

    for element in root.iter():
        if SHADOW_RE.search(element.tag):
            result["shadows"].append(local_name(element.tag))

    for font in root.findall(".//a:latin", NS) + root.findall(".//a:ea", NS) + root.findall(".//a:cs", NS):
        typeface = font.get("typeface")
        if typeface and typeface not in ALLOWED_FONTS and not typeface.startswith("+"):
            result["fonts"].append(typeface)

    for text_node in root.findall(".//a:t", NS):
        text = text_node.text or ""
        if WATERMARK_RE.search(text):
            result["watermark_text"].append(text)

    for run_pr in root.findall(".//a:rPr", NS) + root.findall(".//a:defRPr", NS):
        size = attr_int(run_pr, "sz")
        if size is None:
            continue
        if size < MIN_FONT_HARD:
            result["font_sizes_below_10pt"].append({"size_pt": size / 100})
        elif size < MIN_FONT_REVIEW:
            result["font_sizes_below_12pt"].append({"size_pt": size / 100})

    for shape in root.findall(".//p:sp", NS):
        body_pr = shape.find("./p:txBody/a:bodyPr", NS)
        if body_pr is None:
            continue
        if not element_text(shape).strip():
            continue
        l_ins = attr_int(body_pr, "lIns")
        if not near_target(l_ins):
            result["shape_insets"].append(
                {
                    "shape": shape_name(shape),
                    "lIns": l_ins,
                    "expected": TARGET_INSET_EMU,
                }
            )
        if body_pr.get("wrap") not in {"square"}:
            result["shape_wrap_warnings"].append(
                {
                    "shape": shape_name(shape),
                    "wrap": body_pr.get("wrap"),
                    "expected": "square",
                }
            )

    for idx, cell_pr in enumerate(root.findall(".//a:tcPr", NS), start=1):
        mar_l = attr_int(cell_pr, "marL")
        # Empty cells are common in layout tables, but PowerPoint does not expose
        # a stable parent link in ElementTree. Keep this conservative check.
        if not near_target(mar_l):
            result["table_cell_margins"].append(
                {
                    "cell_index": idx,
                    "marL": mar_l,
                    "expected": TARGET_INSET_EMU,
                }
            )

    candidates = text_object_candidates(root)
    for i, first in enumerate(candidates):
        for second in candidates[i + 1 :]:
            overlap = intersection_area(first["bbox"], second["bbox"])
            if overlap < MIN_OVERLAP_AREA_EMU2:
                continue
            smaller = min(first["area"], second["area"])
            if smaller <= 0 or overlap / smaller < MIN_OVERLAP_RATIO:
                continue
            result["possible_text_overlaps"].append(
                {
                    "first": first["name"],
                    "first_text": first["text_sample"],
                    "second": second["name"],
                    "second_text": second["text_sample"],
                    "overlap_ratio_of_smaller": round(overlap / smaller, 3),
                }
            )

    result["shadows"] = sorted(set(result["shadows"]))
    result["fonts"] = sorted(set(result["fonts"]))
    result["watermark_text"] = sorted(set(result["watermark_text"]))
    return result


def audit_pptx(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".pptx":
        raise ValueError("Expected a .pptx file")

    slides = []
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            (
                name
                for name in zf.namelist()
                if name.startswith("ppt/slides/slide") and name.endswith(".xml")
            ),
            key=slide_sort_key,
        )
        for name in slide_names:
            slides.append(audit_slide(zf.read(name), name))

    summary = {
        "file": str(path),
        "slide_count": len(slides),
        "slides_with_shadows": sum(1 for slide in slides if slide["shadows"]),
        "slides_with_non_yahei_fonts": sum(1 for slide in slides if slide["fonts"]),
        "slides_with_notebooklm_text": sum(1 for slide in slides if slide["watermark_text"]),
        "slides_with_font_below_10pt": sum(1 for slide in slides if slide["font_sizes_below_10pt"]),
        "slides_with_font_below_12pt_review": sum(1 for slide in slides if slide["font_sizes_below_12pt"]),
        "slides_with_shape_inset_warnings": sum(1 for slide in slides if slide["shape_insets"]),
        "slides_with_shape_wrap_warnings": sum(1 for slide in slides if slide["shape_wrap_warnings"]),
        "slides_with_table_margin_warnings": sum(1 for slide in slides if slide["table_cell_margins"]),
        "slides_with_possible_text_overlap_warnings": sum(1 for slide in slides if slide["possible_text_overlaps"]),
    }
    return {"summary": summary, "slides": slides}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit PPTX against PDF-to-editable-PPT requirements.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true", help="Print full JSON details.")
    args = parser.parse_args()

    try:
        report = audit_pptx(args.pptx)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        summary = report["summary"]
        for key, value in summary.items():
            print(f"{key}: {value}")
        review = summary["slides_with_font_below_12pt_review"] + summary[
            "slides_with_possible_text_overlap_warnings"
        ]
        hard_warnings = [
            summary["slides_with_shadows"],
            summary["slides_with_non_yahei_fonts"],
            summary["slides_with_notebooklm_text"],
            summary["slides_with_font_below_10pt"],
            summary["slides_with_shape_inset_warnings"],
            summary["slides_with_shape_wrap_warnings"],
            summary["slides_with_table_margin_warnings"],
        ]
        if any(hard_warnings) or review:
            print("Result: warnings found. Run with --json for details.")
        else:
            print("Result: no static warnings found.")

    return 1 if any(
        report["summary"][key]
        for key in (
            "slides_with_shadows",
            "slides_with_non_yahei_fonts",
            "slides_with_notebooklm_text",
            "slides_with_font_below_10pt",
            "slides_with_shape_inset_warnings",
            "slides_with_shape_wrap_warnings",
            "slides_with_table_margin_warnings",
        )
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
