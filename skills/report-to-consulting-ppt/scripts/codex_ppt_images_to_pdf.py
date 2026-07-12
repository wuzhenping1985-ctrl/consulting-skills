#!/usr/bin/env python3
"""Convert a codex-ppt origin_image directory into a slide-like PDF."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

SLIDE_RE = re.compile(r"^slide_(\d+)\.(png|jpe?g)$", re.IGNORECASE)


def slide_images(deck_dir: Path) -> list[Path]:
    origin = deck_dir / "origin_image"
    if not origin.exists():
        raise SystemExit(f"origin_image directory not found: {origin}")
    found: list[tuple[int, Path]] = []
    for path in origin.iterdir():
        if not path.is_file():
            continue
        match = SLIDE_RE.match(path.name)
        if match:
            found.append((int(match.group(1)), path))
    if not found:
        raise SystemExit(f"No slide_XX.png/jpg files found in: {origin}")
    found.sort(key=lambda item: item[0])
    expected = list(range(found[0][0], found[0][0] + len(found)))
    actual = [num for num, _ in found]
    if actual != expected:
        raise SystemExit(f"Slide image numbering is not continuous: {actual}")
    return [path for _, path in found]


def image_to_rgb(path: Path):
    try:
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Pillow is required for image-to-PDF conversion. Install the copied "
            "Codex PPT requirements or run this script with the Codex bundled Python."
        ) from exc
    image = Image.open(path)
    if image.mode == "RGB":
        return image.copy()
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, "white")
        alpha = image.getchannel("A") if "A" in image.getbands() else None
        background.paste(image.convert("RGB"), mask=alpha)
        return background
    return image.convert("RGB")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert codex-ppt slide images to a PDF")
    parser.add_argument("deck_dir", help="Deck project directory containing origin_image/")
    parser.add_argument("--out", required=True, help="Output PDF path")
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    paths = slide_images(deck_dir)

    images = [image_to_rgb(path) for path in paths]
    out.parent.mkdir(parents=True, exist_ok=True)
    first, rest = images[0], images[1:]
    first.save(out, "PDF", resolution=144.0, save_all=True, append_images=rest)
    for image in images:
        image.close()
    print(f"Wrote {len(paths)} pages: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
