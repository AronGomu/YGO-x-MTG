from pathlib import Path
import re
import time
import urllib.parse
import requests

ROOT = Path(__file__).resolve().parents[1] / 'MSE_projects'
API = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="

NAME_MAP = {
    # Burning Abyss: official Yu-Gi-Oh names
    "Alich, Burning Abyss": "Alich, Malebranche of the Burning Abyss",
    "Barbar, Burning Abyss": "Barbar, Malebranche of the Burning Abyss",
    "Cagna, Burning Abyss": "Cagna, Malebranche of the Burning Abyss",
    "Calcab, Burning Abyss": "Calcab, Malebranche of the Burning Abyss",
    "Cir, Burning Abyss": "Cir, Malebranche of the Burning Abyss",
    "Draghig, Burning Abyss": "Draghig, Malebranche of the Burning Abyss",
    "Farfa, Burning Abyss": "Farfa, Malebranche of the Burning Abyss",
    "Graff, Burning Abyss": "Graff, Malebranche of the Burning Abyss",
    "Libic, Burning Abyss": "Libic, Malebranche of the Burning Abyss",
    "Rubic, Burning Abyss": "Rubic, Malebranche of the Burning Abyss",
    "Scarm, Burning Abyss": "Scarm, Malebranche of the Burning Abyss",
    "Dante, Traveller of the Burning Abyss": "Dante, Traveler of the Burning Abyss",
    "Dante, Voyageur de l'Abîme Ardent": "Dante, Traveler of the Burning Abyss",
    "Virgil, Rock Star of the Burning Abyss": "Virgil, Rock Star of the Burning Abyss",
    "Beatrice, Lady of the Eternal": "Beatrice, Lady of the Eternal",
    "Fire Lake of the Burning Abyss": "Fire Lake of the Burning Abyss",

    # French utility card names -> official English names
    "Compétence de Percée": "Breakthrough Skill",
    "Corbeau D.D.": "D.D. Crow",
    "Dispositif d'Évacuation Obligatoire": "Compulsory Evacuation Device",
    "Double Tornade": "Twin Twisters",
    "Enterrement Précipité": "Foolish Burial",
    "Explosion Ailée du Phénix": "Phoenix Wing Wind Blast",
    "Fusion Instantanée": "Instant Fusion",
    "Gobelin Parvenu": "Upstart Goblin",
    "Guide des Enfers": "Tour Guide From the Underworld",
    "Hommage Torrentiel": "Torrential Tribute",
    "Livre de l'Éclipse": "Book of Eclipse",
    "Livre de la Lune": "Book of Moon",
    "Mathématicien": "Mathematician",
    "Maxx « C »": "Maxx \"C\"",
    "Préparation des Rites": "Preparation of Rites",
    "Renaissance du Monstre": "Monster Reborn",
    "Super Polymérisation": "Super Polymerization",
    "Séduction des Ténèbres": "Allure of Darkness",
    "Trou Noir": "Dark Hole",
    "Typhon d'Espace Mystique": "Mystical Space Typhoon",
}

ARCH = {
    "YGO_Burning_Abyss.mse-set": "Burning_Abyss",
    "YGO_Non_Archetype.mse-set": "Cartes_Utilitaires",
    "YGO_Necroz.mse-set": "Necroz",
    "YGO_Shaddoll.mse-set": "Shaddoll",
    "YGO_Spellbook.mse-set": "Spellbook",
}

def slug(s: str) -> str:
    s = s.lower().replace('"', '').replace('«', '').replace('»', '')
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_")

def get_name(text: str) -> str | None:
    m = re.search(r"(?m)^\s*name:\s*(.+)$", text)
    return m.group(1).strip() if m else None

def download(card_name: str, dest: Path):
    r = requests.get(API + urllib.parse.quote(card_name), timeout=30)
    r.raise_for_status()
    data = r.json()["data"][0]
    image_url = data["card_images"][0].get("image_url_cropped") or data["card_images"][0]["image_url"]
    ir = requests.get(image_url, timeout=45)
    ir.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(ir.content)
    return data["name"], image_url

errors = []
updated = 0
for project in sorted(ROOT.glob("YGO_*.mse-set")):
    arch = ARCH.get(project.name, project.stem.removeprefix("YGO_"))
    for card_file in sorted(project.glob("card *")):
        text = card_file.read_text(encoding="utf-8-sig", errors="replace")
        display = get_name(text)
        if not display:
            continue
        query = NAME_MAP.get(display, display)
        out = project / "images" / arch / f"{slug(query)}.jpg"
        if not out.exists():
            try:
                found, _ = download(query, out)
                print(f"DOWNLOADED | {project.name} | {display} -> {found}")
                time.sleep(0.15)
            except Exception as e:
                errors.append(f"{project.name} | {display} -> {query} | {e}")
                print("ERROR | " + errors[-1])
                continue
        rel = out.relative_to(project).as_posix()
        lines = text.splitlines()
        changed = False
        for i, line in enumerate(lines):
            if re.match(r"^\s*image:\s*", line):
                indent = line.split("image:", 1)[0]
                new_line = f"{indent}image: {rel}"
                changed = line != new_line
                lines[i] = new_line
                break
        else:
            lines.append(f"\timage: {rel}")
            changed = True
        if changed:
            card_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            updated += 1
            print(f"UPDATED | {card_file.relative_to(ROOT)} | image: {rel}")

print(f"Done. Updated {updated} card files.")
if errors:
    print("FAILED:")
    for e in errors:
        print("- " + e)
    raise SystemExit(1)
