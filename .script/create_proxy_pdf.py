#!/usr/bin/env python3
"""Create a print-and-cut proxy PDF from MSE rendered card images.

Default behavior:
- scans canonical `MSE_projects/*.mse-set/render` folders only
- puts each card in the PDF 3 times, for playtest proxy sets
- prints at real Magic card size: 2.5 x 3.5 inches
- uses A4 pages, 9 cards per page, separated by 1-pixel gray cut lines

Example:
    python .script/create_proxy_pdf.py

Specific render folder:
    python .script/create_proxy_pdf.py --input MSE_projects/10_YGO_Burning_Abyss.mse-set/render

Default output naming:
    print/burning_abyss_proxies.pdf

One copy per card:
    python .script/create_proxy_pdf.py --copies 1
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

REPO = Path(__file__).resolve().parents[1]
MSE_PROJECTS = REPO / "MSE_projects"
PRINT_DIR = REPO / "print"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

PAGE_SIZES_IN = {
    "a4": (8.27, 11.69),
    "letter": (8.5, 11.0),
}


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def discover_render_folders(inputs: list[Path]) -> list[Path]:
    if inputs:
        french_archive = (MSE_PROJECTS / "French").resolve()
        folders = [
            (path if path.is_absolute() else (REPO / path)).resolve()
            for path in inputs
        ]
        if any(folder.is_relative_to(french_archive) for folder in folders):
            raise ValueError("Frozen French render folders cannot be proxy-PDF inputs")
        return folders
    return sorted(
        path / "render"
        for path in MSE_PROJECTS.glob("*.mse-set")
        if (path / "render").is_dir()
    )


def output_stem_from_render_folders(render_folders: list[Path]) -> str:
    if len(render_folders) == 1:
        project_dir = render_folders[0].parent
        name = project_dir.name
        if name.endswith(".mse-set"):
            name = name[: -len(".mse-set")]
        name = re.sub(r"^YGO_", "", name, flags=re.IGNORECASE)
        name = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
        return name or "cards"
    return "all_cards"


def default_output_path(render_folders: list[Path]) -> Path:
    return PRINT_DIR / f"{output_stem_from_render_folders(render_folders)}_proxies.pdf"


def collect_images(render_folders: list[Path]) -> list[Path]:
    images: list[Path] = []
    for folder in render_folders:
        if not folder.exists():
            raise FileNotFoundError(f"Render folder not found: {folder}")
        images.extend(
            sorted(
                [path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS],
                key=natural_key,
            )
        )
    return images


def paste_card(page: Image.Image, image_path: Path, box: tuple[int, int, int, int]) -> None:
    left, top, width, height = box
    with Image.open(image_path) as raw:
        card = raw.convert("RGB")
        # Fill the exact Magic-card rectangle without stretching. MSE exports should already
        # be the correct ratio; ImageOps.fit is a safety net for odd render sizes.
        card = ImageOps.fit(card, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        page.paste(card, (left, top))


def make_pdf(
    image_paths: list[Path],
    output: Path,
    copies: int,
    dpi: int,
    page_size: str,
    card_width_in: float,
    card_height_in: float,
    separator_px: int,
) -> None:
    page_width_in, page_height_in = PAGE_SIZES_IN[page_size]
    page_w = round(page_width_in * dpi)
    page_h = round(page_height_in * dpi)
    card_w = round(card_width_in * dpi)
    card_h = round(card_height_in * dpi)
    gap = separator_px

    cols = max(1, math.floor((page_w + gap) / (card_w + gap)))
    rows = max(1, math.floor((page_h + gap) / (card_h + gap)))
    per_page = cols * rows

    used_w = cols * card_w + (cols - 1) * gap
    used_h = rows * card_h + (rows - 1) * gap
    margin_x = (page_w - used_w) // 2
    margin_y = (page_h - used_h) // 2

    expanded = [path for path in image_paths for _ in range(copies)]
    pages: list[Image.Image] = []

    for start in range(0, len(expanded), per_page):
        page = Image.new("RGB", (page_w, page_h), "white")
        draw = ImageDraw.Draw(page)
        separator = (160, 160, 160)
        for index, image_path in enumerate(expanded[start : start + per_page]):
            row, col = divmod(index, cols)
            left = margin_x + col * (card_w + gap)
            top = margin_y + row * (card_h + gap)
            paste_card(page, image_path, (left, top, card_w, card_h))
        if gap > 0:
            cards_on_page = min(per_page, len(expanded) - start)
            rows_on_page = math.ceil(cards_on_page / cols)
            used_cols = min(cols, cards_on_page)
            for col in range(1, used_cols):
                x = margin_x + col * card_w + (col - 1) * gap
                draw.rectangle([x, margin_y, x + gap - 1, margin_y + rows_on_page * card_h + (rows_on_page - 1) * gap - 1], fill=separator)
            for row in range(1, rows_on_page):
                y = margin_y + row * card_h + (row - 1) * gap
                width_cols = cols if row < rows_on_page - 1 else ((cards_on_page - 1) % cols) + 1
                width_cols = cols if row < rows_on_page else width_cols
                draw.rectangle([margin_x, y, margin_x + width_cols * card_w + (width_cols - 1) * gap - 1, y + gap - 1], fill=separator)
        pages.append(page)

    if not pages:
        raise RuntimeError("No pages generated; no card images were found.")

    output.parent.mkdir(parents=True, exist_ok=True)
    first, rest = pages[0], pages[1:]
    first.save(output, "PDF", resolution=dpi, save_all=True, append_images=rest)

    print(f"Created: {output}")
    print(f"Input cards: {len(image_paths)}")
    print(f"Copies per card: {copies}")
    print(f"Total proxy cards: {len(expanded)}")
    print(f"Page size: {page_size.upper()} at {dpi} DPI")
    print(f"Card size: {card_width_in} x {card_height_in} inches")
    print(f"Grid: {cols} x {rows} = {per_page} cards/page")
    print(f"Separator: {separator_px}px gray line between cards")
    print(f"Pages: {len(pages)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a printable Magic-card proxy PDF from MSE render images.")
    parser.add_argument("--input", "-i", action="append", type=Path, help="Render folder to read. Can be passed multiple times. Defaults to all MSE_projects/**/render folders.")
    parser.add_argument("--output", "-o", type=Path, help="Output PDF path. Default: print/[archetype]_proxies.pdf, inferred from the render folder's .mse-set name.")
    parser.add_argument("--copies", "-c", type=int, default=3, help="Copies of each card to include. Default: 3.")
    parser.add_argument("--dpi", type=int, default=300, help="Print resolution. Default: 300.")
    parser.add_argument("--page-size", choices=sorted(PAGE_SIZES_IN), default="a4", help="PDF page size. Default: a4.")
    parser.add_argument("--card-width", type=float, default=2.5, help="Card width in inches. Default: 2.5.")
    parser.add_argument("--card-height", type=float, default=3.5, help="Card height in inches. Default: 3.5.")
    parser.add_argument("--separator-px", type=int, default=1, help="Gray separator line width between cards, in pixels. Default: 1.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.copies < 1:
        raise ValueError("--copies must be at least 1")
    render_folders = discover_render_folders(args.input or [])
    images = collect_images(render_folders)
    if not images:
        searched = "\n".join(str(folder) for folder in render_folders)
        raise RuntimeError(f"No render images found. Searched:\n{searched}")
    if args.output:
        output = args.output if args.output.is_absolute() else (REPO / args.output)
    else:
        output = default_output_path(render_folders)
    make_pdf(
        image_paths=images,
        output=output,
        copies=args.copies,
        dpi=args.dpi,
        page_size=args.page_size,
        card_width_in=args.card_width,
        card_height_in=args.card_height,
        separator_px=args.separator_px,
    )


if __name__ == "__main__":
    main()
