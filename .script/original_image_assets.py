"""Shared paths and naming for the repository's original Yu-Gi-Oh! artwork library."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_IMAGES_ROOT = REPO_ROOT / "assets" / "original_images"


def safe_slug(value: str) -> str:
    """Return the lowercase filesystem slug used by artwork folders and files."""
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", ascii_value)).strip("_")


def archetype_folder(card: dict) -> str:
    """Use Yu-Gi-Oh! archetype metadata, never the cube document/project grouping."""
    return safe_slug(card.get("archetype") or "non_archetype")


def original_image_path(card: dict, extension: str = ".jpg") -> Path:
    """Return the canonical source-art path for a YGOPRODeck card record."""
    suffix = extension if extension.startswith(".") else f".{extension}"
    return ORIGINAL_IMAGES_ROOT / archetype_folder(card) / f"{safe_slug(card['name'])}{suffix.lower()}"
