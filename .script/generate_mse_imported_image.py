#!/usr/bin/env python3
"""Generate a project-local MSE image from a centralized source-art file.

Original artwork remains under original_images/. This helper creates an
imported/resized PNG under the target project's mse_images/ folder so card files
never point directly at the source JPG.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


def next_image_path(project: Path) -> Path:
    image_dir = project / "mse_images"
    image_dir.mkdir(parents=True, exist_ok=True)
    used = set()
    for path in image_dir.glob("image*.png"):
        match = re.fullmatch(r"image(\d+)\.png", path.name)
        if match:
            used.add(int(match.group(1)))
    index = 1
    while index in used:
        index += 1
    return image_dir / f"image{index}.png"


def resize_cover(source: Path, output: Path, width: int, height: int) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        src_w, src_h = image.size
        scale = max(width / src_w, height / src_h)
        resized = image.resize((round(src_w * scale), round(src_h * scale)), Image.Resampling.LANCZOS)
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        cropped = resized.crop((left, top, left + width, top + height))
        cropped.save(output, "PNG")


def update_card_image(card_file: Path, image_name: str) -> None:
    text = card_file.read_text(encoding="utf-8-sig")
    if re.search(r"^[ \t]*image:[ \t]*.*$", text, flags=re.M):
        text = re.sub(r"^([ \t]*image:[ \t]*).*$", rf"\g<1>{image_name}", text, flags=re.M)
    else:
        text = text.replace("card:\n", f"card:\n\timage: {image_name}\n", 1)
    card_file.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an MSE-safe mse_images/imageN.png from source art.")
    parser.add_argument("project", type=Path, help="Path to the .mse-set project folder")
    parser.add_argument("source_image", type=Path, help="Source image to import/resize")
    parser.add_argument("--card-file", type=Path, help="Optional card file to update to image: imageN.png")
    parser.add_argument("--width", type=int, default=316, help="Imported art width; MSE observed default is 316")
    parser.add_argument("--height", type=int, default=231, help="Imported art height; MSE observed default is 231")
    args = parser.parse_args()

    project = args.project.resolve()
    source = args.source_image.resolve()
    if not project.is_dir():
        raise SystemExit(f"Project folder not found: {project}")
    if not source.is_file():
        raise SystemExit(f"Source image not found: {source}")

    output = next_image_path(project)
    resize_cover(source, output, args.width, args.height)

    if args.card_file:
        card_file = args.card_file
        if not card_file.is_absolute():
            card_file = project / card_file
        if not card_file.is_file():
            raise SystemExit(f"Card file not found: {card_file}")
        update_card_image(card_file, output.relative_to(project).as_posix())

    print(output.relative_to(project).as_posix())


if __name__ == "__main__":
    main()
