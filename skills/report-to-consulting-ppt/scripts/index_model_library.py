#!/usr/bin/env python3
"""Print a compact index of PPTX model-library decks."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

SKIP_TEXT_RE = re.compile(
    r"(框架搭建系列|配色说明|版权局|欢迎关注|字体|一键修改|一键去除|CONTENTS|目录|开悟思维|复制到自己PPT)",
    re.IGNORECASE,
)


def local_slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 999999


def parse_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except Exception:
        return None


def text_of(element: ET.Element) -> str:
    return "".join(t.text or "" for t in element.findall(".//a:t", NS)).strip()


def layout_names(zf: zipfile.ZipFile) -> list[str]:
    names = []
    layouts = sorted(
        (
            name
            for name in zf.namelist()
            if name.startswith("ppt/slideLayouts/slideLayout") and name.endswith(".xml")
        ),
        key=lambda value: int(Path(value).stem.replace("slideLayout", "")),
    )
    for layout in layouts:
        root = parse_xml(zf, layout)
        if root is None:
            continue
        c_sld = root.find("p:cSld", NS)
        if c_sld is not None and c_sld.get("name"):
            names.append(c_sld.get("name", ""))
    return names


def slide_title(root: ET.Element) -> str:
    fallback = ""
    for shape in root.findall(".//p:sp", NS):
        text = " / ".join(text_of(shape).split())
        if not text or len(text) > 120:
            continue
        ph = shape.find(".//p:ph", NS)
        ph_type = ph.get("type") if ph is not None else ""
        if ph_type in {"title", "ctrTitle"}:
            return text
        if not fallback:
            fallback = text
    return fallback


def index_deck(path: Path, max_titles: int) -> dict:
    with zipfile.ZipFile(path) as zf:
        slides = sorted(
            (
                name
                for name in zf.namelist()
                if name.startswith("ppt/slides/slide") and name.endswith(".xml")
            ),
            key=local_slide_number,
        )
        titles = []
        for slide in slides:
            root = parse_xml(zf, slide)
            if root is None:
                continue
            title = slide_title(root)
            if not title or SKIP_TEXT_RE.search(title):
                continue
            titles.append((local_slide_number(slide), title))
            if len(titles) >= max_titles:
                break
        return {
            "file": path.name,
            "slides": len(slides),
            "layouts": layout_names(zf),
            "candidate_titles": titles,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Index report-to-consulting-ppt model library.")
    parser.add_argument(
        "library",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "model-library",
    )
    parser.add_argument("--max-titles", type=int, default=12)
    args = parser.parse_args()

    for deck in sorted(args.library.glob("*.pptx")):
        item = index_deck(deck, args.max_titles)
        print(f"\n{item['file']} ({item['slides']} slides)")
        print("Layouts:", " | ".join(item["layouts"][:12]))
        print("Candidate titles:")
        for slide_no, title in item["candidate_titles"]:
            print(f"  - slide {slide_no}: {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
