# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", "node_modules", "original_cards", "original_images", "print"}
SKIP_SUFFIX = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".pdf",
    ".zip",
    ".exe",
    ".com",
    ".dll",
    ".pyc",
}
TEXT_SUFFIX = {
    ".md",
    ".py",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".css",
    ".html",
    ".js",
    ".ts",
    ".csv",
}


def is_target(p: Path) -> bool:
    if any(part in SKIP_DIRS for part in p.parts):
        return False
    if p.suffix.lower() in SKIP_SUFFIX:
        return False
    if p.suffix.lower() in TEXT_SUFFIX:
        return True
    if p.name.startswith("card ") or p.name == "set":
        return True
    return False


def transform(text: str) -> str:
    reps = [
        (r"On Send Grave", "On Send Grave"),
        (r"On Send Grave", "On Send Grave"),
        (r"\bGYD\b", "Grave"),
        (r"Graves", "Graves"),
        (r"Graves", "Graves"),
        (r"Grave", "Grave"),
        (r"Grave", "Grave"),
        (r"Grave", "Grave"),
        (r"Grave", "Grave"),
    ]
    out = text
    for pat, rep in reps:
        out = re.sub(pat, rep, out)
    out = re.sub(r"\bGY\b", "Grave", out)
    out = out.replace("Grave", "Grave")
    return out


def main() -> None:
    changed = []
    for p in root.rglob("*"):
        if not p.is_file() or not is_target(p):
            continue
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        bom = raw.startswith(b"\xef\xbb\xbf")
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            continue
        new = transform(text)
        if new == text:
            continue
        data = new.encode("utf-8")
        if bom:
            data = b"\xef\xbb\xbf" + data
        p.write_bytes(data)
        changed.append(p.relative_to(root).as_posix())

    print("changed files", len(changed))
    for c in sorted(changed):
        print(c)

    residual_files = []
    for p in root.rglob("*"):
        if not p.is_file() or not is_target(p):
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if re.search(r"Grave|Grave|\bGYD\b|\bGY\b|On Send Grave(?!D)", t, re.I):
            # still report case-sensitive Grave
            if (
                re.search(r"Grave|Grave", t, re.I)
                or re.search(r"\bGYD\b", t)
                or re.search(r"\bGY\b", t)
            ):
                residual_files.append(p.relative_to(root).as_posix())

    print("residual files", len(residual_files))
    for c in residual_files[:50]:
        print(c)


if __name__ == "__main__":
    main()
