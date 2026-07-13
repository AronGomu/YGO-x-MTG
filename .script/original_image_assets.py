"""Shared paths and naming for the repository's original Yu-Gi-Oh! artwork library."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_IMAGES_ROOT = REPO_ROOT / "original_images"


def safe_slug(value: str) -> str:
    """Return the lowercase filesystem slug used for project-local MSE images."""
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", ascii_value)).strip("_")


def card_filename(name: str, extension: str) -> str:
    """Return the official card name made safe for Windows, plus an extension."""
    replacements = {
        ":": " -",
        '"': "'",
        "/": " - ",
        "\\": " - ",
        "?": "",
        "*": "",
        "<": "",
        ">": "",
        "|": "-",
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    stem = re.sub(r"\s+", " ", name).strip().rstrip(".")
    suffix = extension if extension.startswith(".") else f".{extension}"
    return stem + suffix.lower()


def card_type_folder(card: dict) -> str:
    """Return the same card-type folder used by original_cards records."""
    card_type = str(card.get("type", "")).casefold()
    for marker, folder in (
        ("spell", "Spell"),
        ("trap", "Trap"),
        ("link", "Link"),
        ("xyz", "Xyz"),
        ("synchro", "Synchro"),
        ("fusion", "Fusion"),
        ("ritual", "Ritual"),
    ):
        if marker in card_type:
            return folder
    if "normal" in card_type:
        return "Normal Monster"
    if "monster" in card_type:
        return "Effect Monster"
    raise ValueError(f"Unsupported Yu-Gi-Oh! card type: {card.get('type')!r}")


def original_image_path(card: dict, extension: str = ".jpg") -> Path:
    """Return the canonical source-art path for a YGOPRODeck card record."""
    return ORIGINAL_IMAGES_ROOT / card_type_folder(card) / card_filename(
        card["name"], extension
    )
