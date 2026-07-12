from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "10_YGO_Burning_Abyss.mse-set"
DOCUMENT = ROOT / "docs" / "10_archetype_burning_abyss.md"


def field(text: str, name: str) -> str:
    match = re.search(rf"(?m)^\t{name}:[ \t]*(.*)$", text)
    return match.group(1).strip() if match else ""


def plain_mse_value(value: str) -> str:
    parts = re.findall(r"<word-list-[^>]+>(.*?)</word-list-[^>]+>", value)
    if parts:
        return " ".join(part for part in parts if part).strip()
    return re.sub(r"<[^>]+>", "", value).strip()


def markdown_cost(value: str) -> str:
    return "".join(f"{{{token}}}" for token in re.findall(r"\d+|[A-Z]", value))


def markdown_rule(line: str) -> str:
    line = re.sub(r"<i-auto>(.*?)</i-auto>", r"\1", line)
    line = re.sub(r"<i>(.*?)</i>", r"*\1*", line)
    line = re.sub(r"<b>(.*?)</b>", r"**\1**", line)
    line = re.sub(r"<sym-auto>(.*?)</sym-auto>", r"\1", line)
    return re.sub(r"<[^>]+>", "", line).strip()


def card_body(card_text: str) -> str:
    super_type = plain_mse_value(field(card_text, "super_type"))
    sub_type = plain_mse_value(field(card_text, "sub_type"))
    type_line = f"{super_type} — {sub_type}" if sub_type else super_type

    lines = [f"**Coût :** {markdown_cost(field(card_text, 'casting_cost'))}", "", type_line]
    power = field(card_text, "power")
    toughness = field(card_text, "toughness")
    if power or toughness:
        lines += ["", f"**{power} / {toughness}**"]

    rule_match = re.search(r"(?m)^\trule_text:[ \t]*\n((?:\t\t[^\n]*\n?)*)", card_text)
    if rule_match:
        rules = [markdown_rule(line[2:]) for line in rule_match.group(1).splitlines() if line.strip()]
        for rule in rules:
            lines += ["", rule]

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
    includes = re.findall(r"(?m)^include_file:\s*(.+)$", set_text)
    document = DOCUMENT.read_text(encoding="utf-8-sig")

    for include in includes:
        card_text = (PROJECT / include).read_text(encoding="utf-8-sig")
        name = field(card_text, "name")
        heading = re.search(rf"(?m)^## .+ => {re.escape(name)}$", document)
        if not heading:
            raise ValueError(f"Missing card section for {name!r}")
        next_separator = document.find("\n---", heading.end())
        if next_separator < 0:
            raise ValueError(f"Missing section separator after {name!r}")
        document = document[: heading.end()] + "\n\n" + card_body(card_text) + document[next_separator:]

    DOCUMENT.write_text("\ufeff" + document.lstrip("\ufeff"), encoding="utf-8")
    print(f"Synchronized {len(includes)} cards into {DOCUMENT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
