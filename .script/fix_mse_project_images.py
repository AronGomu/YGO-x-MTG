#!/usr/bin/env python3
"""Normalize an MSE folder project to project-local mse_images/imageN.png files.

This addresses MSE GUI Save failures observed when cards reference centralized
source JPGs or legacy nested source folders. Each non-empty image field outside
mse_images/ is converted to a resized PNG in that folder and the card file is
updated. Includes are sorted by visible name and collection numbers are rewritten.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps

IMAGE_FIELDS = ("image", "image_2", "mainframe_image", "mainframe_image_2")
MSE_IMAGE_RE = re.compile(r"image\d+\.png")
CODE_RE = re.compile(r"^([ \t]*card_code_text(?:_[23])?:[ \t]*)(.*)$", re.M)


def next_image_path(project: Path) -> Path:
    image_dir = project / "mse_images"
    image_dir.mkdir(parents=True, exist_ok=True)
    used = set()
    for path in image_dir.glob("image*.png"):
        match = MSE_IMAGE_RE.fullmatch(path.name)
        if match:
            used.add(int(path.stem.replace("image", "")))
    index = 1
    while index in used:
        index += 1
    return image_dir / f"image{index}.png"


def resize_cover(source: Path, output: Path, width: int = 316, height: int = 231) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        src_w, src_h = image.size
        scale = max(width / src_w, height / src_h)
        resized = image.resize((round(src_w * scale), round(src_h * scale)), Image.Resampling.LANCZOS)
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        resized.crop((left, top, left + width, top + height)).save(output, "PNG")


def read_includes(set_text: str) -> list[str]:
    return [line.split(":", 1)[1].strip() for line in set_text.splitlines() if line.startswith("include_file:")]


def read_card_name(text: str, fallback: str) -> str:
    match = re.search(r"^[ \t]*name:[ \t]*(.*)$", text, re.M)
    return match.group(1).strip() if match else fallback


def normalize_images(project: Path, card_file: Path, text: str) -> tuple[str, list[str]]:
    changed = []

    def replace_field(match: re.Match[str]) -> str:
        indent, field, value = match.group(1), match.group(2), match.group(3).strip()
        if not value or value.startswith("<"):
            return match.group(0)
        if value.startswith("mse_images/") and MSE_IMAGE_RE.fullmatch(Path(value).name):
            return match.group(0)
        source = project / value
        if not source.exists():
            raise FileNotFoundError(f"{card_file.name}: missing referenced {field}: {value}")
        output = next_image_path(project)
        resize_cover(source, output)
        relative_output = output.relative_to(project).as_posix()
        changed.append(f"{card_file.name}: {field} {value} -> {relative_output}")
        return f"{indent}{field}: {relative_output}"

    pattern = r"^([ \t]*)({fields}):[ \t]*(.*)$".format(fields="|".join(map(re.escape, IMAGE_FIELDS)))
    new_text = re.sub(pattern, replace_field, text, flags=re.M)
    return new_text, changed


def renumber(text: str, index: int, total: int) -> str:
    code = f"{index:03d}/{total:03d}"

    def repl(match: re.Match[str]) -> str:
        prefix, old = match.group(1), match.group(2).strip()
        suffix_match = re.match(r"\d+/\d+\s+(.+)$", old)
        suffix = suffix_match.group(1).strip() if suffix_match else "C"
        return f"{prefix}{code} {suffix}"

    if CODE_RE.search(text):
        return CODE_RE.sub(repl, text)
    return text.rstrip() + f"\n\tcard_code_text: {code} C\n"


def fix_project(project: Path, clean_orphans: bool = True) -> list[str]:
    set_path = project / "set"
    if not set_path.exists():
        raise FileNotFoundError(f"Missing set file: {set_path}")
    set_text = set_path.read_text(encoding="utf-8-sig")
    includes = read_includes(set_text)
    log = []
    items = []
    for include in includes:
        card_path = project / include
        if not card_path.exists():
            raise FileNotFoundError(f"Missing included card file: {card_path}")
        text = card_path.read_text(encoding="utf-8-sig")
        text, image_log = normalize_images(project, card_path, text)
        log.extend(image_log)
        name = read_card_name(text, include)
        items.append((name.lower(), name, include, card_path, text))

    items.sort(key=lambda item: item[0])
    total = len(items)
    active = {include for _, _, include, _, _ in items}
    for index, (_, _, _, card_path, text) in enumerate(items, start=1):
        card_path.write_text(renumber(text, index, total), encoding="utf-8")

    lines = [line for line in set_text.splitlines(True) if not line.startswith("include_file:")]
    insert_at = next((i for i, line in enumerate(lines) if line.startswith("version_control:")), len(lines))
    lines[insert_at:insert_at] = [f"include_file: {include}\n" for _, _, include, _, _ in items]
    set_path.write_text("".join(lines), encoding="utf-8")

    if clean_orphans:
        for child in project.iterdir():
            if child.is_file() and child.name.startswith("card ") and child.name not in active:
                child.unlink()
                log.append(f"removed orphan {child.name}")
    return log


def backup_project(project: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = project.with_name(project.name.replace(".mse-set", f".imagefix-backup-{stamp}.mse-set"))
    shutil.copytree(project, backup)
    return backup


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize included MSE card images to mse_images/imageN.png files.")
    parser.add_argument("projects", nargs="+", type=Path)
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--keep-orphans", action="store_true")
    args = parser.parse_args()

    for raw in args.projects:
        project = raw.resolve()
        if args.backup:
            print(f"backup: {backup_project(project)}")
        print(f"project: {project}")
        log = fix_project(project, clean_orphans=not args.keep_orphans)
        for entry in log:
            print(f"  {entry}")


if __name__ == "__main__":
    main()
