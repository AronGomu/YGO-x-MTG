"""Refresh existing original_cards records from Konami's official database."""

from __future__ import annotations

import argparse
import html as html_module
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests
from lxml import html

from original_image_assets import card_filename

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "original_cards"
OFFICIAL = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; YGO-x-MTG card documentation)"}
NAME_OVERRIDES = {"ddcrow": "D.D. Crow"}
LINK_DIRECTIONS = {
    "1": "Bottom-Left", "2": "Bottom", "3": "Bottom-Right", "4": "Left",
    "6": "Right", "7": "Top-Left", "8": "Top", "9": "Top-Right",
}


def normalize(value: str) -> str:
    value = value.replace("«", '"').replace("»", '"').replace("’", "'")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", value)


def original_card_names() -> list[str]:
    names: dict[str, str] = {}
    for path in sorted(OUTPUT.rglob("*.md")):
        heading = next(
            (
                line.removeprefix("# ").strip()
                for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.startswith("# ")
            ),
            "",
        )
        if heading:
            names.setdefault(normalize(heading), heading)
    return list(names.values())


def canonical_card(name: str) -> dict:
    lookup_name = NAME_OVERRIDES.get(normalize(name), name)
    for parameter in ("name", "fname"):
        response = requests.get(
            "https://db.ygoprodeck.com/api/v7/cardinfo.php",
            params={parameter: lookup_name}, headers=HEADERS, timeout=60,
        )
        if response.ok:
            cards = response.json().get("data", [])
            exact = [card for card in cards if normalize(card["name"]) == normalize(lookup_name)]
            if exact:
                return exact[0]
            if cards:
                return cards[0]
    raise RuntimeError(f"No canonical match for {name!r}")


def canonical_cards() -> list[dict]:
    response = requests.get(
        "https://db.ygoprodeck.com/api/v7/cardinfo.php",
        headers={**HEADERS, "Accept-Encoding": "gzip"}, timeout=180,
    )
    response.raise_for_status()
    index = {normalize(card["name"]): card for card in response.json()["data"]}
    selected = []
    for original_name in original_card_names():
        key = normalize(original_name)
        card = index.get(normalize(NAME_OVERRIDES.get(key, original_name)))
        if not card:
            raise RuntimeError(f"No canonical match for {original_name!r}")
        selected.append(card)
    return sorted(selected, key=lambda card: card["name"].casefold())


def xpath_class(name: str, anywhere: bool = False) -> str:
    start = "//*" if anywhere else ".//*"
    return f'{start}[contains(concat(" ", normalize-space(@class), " "), " {name} ")]'


def element_text(element, breaks: bool = False) -> str:
    element = deepcopy(element)
    if breaks:
        for br in element.xpath(".//br"):
            br.tail = "\n" + (br.tail or "")
    value = html_module.unescape("".join(element.itertext())).replace("\r", "")
    if not breaks:
        return " ".join(value.split())
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in value.split("\n")]
    return "\n".join(line for line in lines if line)


def class_text(row, name: str) -> str:
    elements = row.xpath(xpath_class(name))
    return element_text(elements[0]) if elements else ""


def fetch_official(card: dict) -> dict:
    for attempt in range(5):
        try:
            response = requests.get(
                OFFICIAL,
                params={"ope": 1, "keyword": card["name"], "stype": 1, "request_locale": "en"},
                headers=HEADERS, timeout=60,
            )
            response.raise_for_status()
            break
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    time.sleep(0.1)
    document = html.fromstring(response.content)
    rows = document.xpath(xpath_class("t_row", anywhere=True))
    rows = [row for row in rows if normalize(class_text(row, "card_name")) == normalize(card["name"])]
    if len(rows) != 1:
        found = [class_text(row, "card_name") for row in document.xpath(xpath_class("t_row", anywhere=True))]
        raise RuntimeError(f"Official exact match failed for {card['name']!r}; found {found}")
    row = rows[0]

    text_elements = row.xpath(xpath_class("box_card_text"))
    type_line = class_text(row, "card_info_species_and_other_item").strip("[] ")
    parts = [part.strip() for part in type_line.split("／") if part.strip()]
    attribute = class_text(row, "box_card_attribute")
    cid = row.xpath('string(.//input[@class="cid"]/@value)').strip()
    link_arrows = []
    images = row.xpath(xpath_class("box_card_linkmarker") + '//img[contains(@src, "link_pc/link")]')
    if images:
        marker = re.search(r"link([1-9]+)\.png", images[0].get("src", ""))
        if marker:
            link_arrows = [LINK_DIRECTIONS[x] for x in marker.group(1) if x in LINK_DIRECTIONS]
    return {
        "name": class_text(row, "card_name"),
        "attribute": attribute,
        "property": class_text(row, "box_card_effect") or ("Normal" if attribute in {"SPELL", "TRAP"} else ""),
        "level_rank": class_text(row, "box_card_level_rank"),
        "link_rating": class_text(row, "box_card_linkmarker"),
        "parts": parts,
        "atk": re.sub(r"^ATK\s*", "", class_text(row, "atk_power")),
        "def": re.sub(r"^DEF\s*", "", class_text(row, "def_power")),
        "link_arrows": link_arrows,
        "text": element_text(text_elements[0], breaks=True) if text_elements else "",
        "cid": cid,
        "url": f"{OFFICIAL}?ope=2&cid={quote(cid)}&request_locale=en",
    }


def category(card: dict) -> tuple[str, str]:
    if card["attribute"] == "SPELL": return "Spell", "Spell Card"
    if card["attribute"] == "TRAP": return "Trap", "Trap Card"
    for marker, folder in (("Link", "Link"), ("Xyz", "Xyz"), ("Synchro", "Synchro"),
                           ("Fusion", "Fusion"), ("Ritual", "Ritual")):
        if marker in card["parts"]: return folder, f"{folder} Monster"
    if "Effect" in card["parts"] or "Flip" in card["parts"]:
        return "Effect Monster", "Effect Monster"
    return "Normal Monster", "Normal Monster"


def filename(name: str) -> str:
    return card_filename(name, ".md")


def render(card: dict, card_type: str) -> str:
    lines = [f'# {card["name"]}', "", f'- **Card type:** {card_type}']
    if card["attribute"] in {"SPELL", "TRAP"}:
        lines.append(f'- **Property:** {card["property"]}')
    else:
        lines += [f'- **Attribute:** {card["attribute"]}']
        if card["parts"]:
            lines += [f'- **Monster type:** {card["parts"][0]}',
                      f'- **Type line:** {" / ".join(card["parts"])}']
        if card["level_rank"]:
            label, _, value = card["level_rank"].partition(" ")
            lines.append(f'- **{label}:** {value}')
        if card["link_rating"]:
            lines.append(f'- **Link Rating:** {card["link_rating"].partition(" ")[2]}')
        if card["link_arrows"]:
            lines.append(f'- **Link Arrows:** {", ".join(card["link_arrows"])}')
        lines += [f'- **ATK:** {card["atk"] or "—"}',
                  f'- **DEF:** {card["def"] if card["def"] and card["def"] != "-" else "—"}']
    lines += ["", "## Card text", "", card["text"], "", "## Source", "",
              f'- [Official Yu-Gi-Oh! Neuron card database]({card["url"]})',
              f'- **Database CID:** {card["cid"]}', f'- **Retrieved:** {date.today().isoformat()}', ""]
    return "\n".join(lines)


def write_card(card: dict) -> Path:
    folder, card_type = category(card)
    path = OUTPUT / folder / filename(card["name"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(card, card_type), encoding="utf-8", newline="\n")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", help="Fetch and write one original Yu-Gi-Oh! card")
    args = parser.parse_args()
    if args.card:
        path = write_card(fetch_official(canonical_card(args.card)))
        print(path.relative_to(ROOT))
        return

    canonical = canonical_cards()
    cards, failures = [], []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch_official, card): card["name"] for card in canonical}
        for index, future in enumerate(as_completed(futures), 1):
            name = futures[future]
            try:
                cards.append(future.result())
                print(f"[{index:03}/{len(canonical)}] {name}")
            except Exception as error:
                failures.append(f"{name}: {error}")
    if failures:
        raise RuntimeError("\n".join(failures))

    written = set()
    for card in sorted(cards, key=lambda item: item["name"].casefold()):
        path = write_card(card)
        key = str(path).casefold()
        if key in written: raise RuntimeError(f"Filename collision: {path}")
        written.add(key)
    print(f"Wrote {len(cards)} cards to {OUTPUT}")


if __name__ == "__main__":
    main()
