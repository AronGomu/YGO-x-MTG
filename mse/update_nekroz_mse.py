from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "12_YGO_Necroz.mse-set"
SYNCHRO_PROJECT = ROOT / "MSE_projects" / "12_YGO_Necroz_Synchro.mse-set"

CARDS = {
    "nekroz of brionac": ("Ritual Creature", "Warrior", [
        "(1 - Activable Sorcery Hard) Défaussez cette carte : cherchez 1 créature “Nekroz”.",
        "(2 - Activable Sorcery Hard) Mélangez dans le Sideboard 1 créature ciblée qui a été mise en jeu depuis un Sideboard.",
    ]),
    "nekroz of clausolas": ("Ritual Creature", "Warrior", [
        "(1 - Activable Sorcery Hard) Défaussez cette carte : cherchez 1 carte non-créature “Nekroz” avec le sous-type Invocation Ritual.",
        "(2 - Activable Sorcery Hard) La créature ciblée devient 0/1 et perd toutes ses capacités jusqu’à la fin du tour.",
    ]),
    "nekroz of unicore": ("Ritual Creature", "Warrior", [
        "(1 - Activable Sorcery Hard) Défaussez cette carte : renvoyez 1 carte “Nekroz” ciblée depuis votre GY dans votre main.",
        "(2 - Passif) Les créatures mises en jeu depuis un Sideboard perdent toutes leurs capacités.",
    ]),
    "nekroz of trishula": ("Ritual Creature", "Dragon", [
        "(1 - Activable Flash Hard) Défaussez cette carte : contrecarrez 1 sort ou capacité ciblant 1 créature “Nekroz” que vous contrôlez.",
        "(2 - Déclenchable Hard) <b>On Enter</b> — Exilez 1 permanent non-terrain adverse ciblé, 1 carte aléatoire de la main de cet adversaire et 1 carte ciblée de son GY. Cet effet ne se résout que si vous pouvez exiler les 3 cartes.",
    ]),
    "nekroz of valkyrus": ("Ritual Creature", "Warrior", [
        "(1 - Activable Flash Hard) Si vous ne contrôlez aucune créature sur le terrain, défaussez cette carte : prévenez toutes les blessures de combat qui devraient vous être infligées ce tour-ci.",
        "(2 - Activable Sorcery Hard) Sacrifiez jusqu’à 2 créatures depuis votre main ou terrain ; piochez 1 carte pour chaque créature sacrifiée ainsi.",
    ]),
    "nekroz of gungnir": ("Ritual Creature", "Dragon", [
        "(1 - Activable Flash Hard) Défaussez cette carte : renvoyez 1 carte “Nekroz” ciblée depuis votre GY dans votre main.",
        "(2 - Activable Flash Hard) Défaussez 1 carte “Nekroz” : 1 créature “Nekroz” ciblée gagne indestructible jusqu’à la fin du tour.",
    ]),
    "nekroz of decisive armor": ("Ritual Creature", "Warrior", [
        "(1 - Activable Flash Hard) Défaussez cette carte : 1 créature “Nekroz” ciblée gagne +2/+2 jusqu’à la fin du tour.",
        "(2 - Activable Sorcery Hard) La créature ciblée gagne -2/-0 jusqu’à la fin du tour.",
    ]),
    "nekroz of catastor": ("Ritual Creature", "Machine", [
        "(1 - Activable Sorcery Hard) Défaussez cette carte : renvoyez sur le terrain 1 créature “Nekroz” ciblée depuis votre GY.",
        "(2 - Passif) Les créatures “Nekroz” que vous contrôlez ont ward 2.",
    ]),
    "shurit strategist of the nekroz": ("Creature", "Warrior", [
        "(1 - Passif) **On Sacrifice** — Pour une Invocation Ritual d’1 créature “Nekroz”, elle peut satisfaire seule son coût de MV.",
        "(2 - Déclenchable Hard) **On Sacrifice** — Cherchez 1 créature “Nekroz”.",
    ]),
    "dance princess of the nekroz": ("Creature", "Wizard", [
        "(1 - Passif) Les adversaires ne peuvent pas répondre à vos sorts “Nekroz” Ritual.",
        "(2 - Passif) Les créatures Ritual “Nekroz” que vous contrôlez ont la défense talismanique.",
        "(3 - Déclenchable Hard) **On Sacrifice** — Renvoyez 1 autre carte “Nekroz” ciblée depuis l’exil dans votre main.",
    ]),
    "great sorcerer of the nekroz": ("Creature", "Wizard", [
        "(1 - Déclenchable Hard) **On Sacrifice** — Cherchez 1 créature Ritual “Nekroz”.",
        "(2 - Déclenchable Hard) Si cette carte est exilée, renvoyez 1 autre carte “Nekroz” ciblée depuis l’exil dans votre main.",
    ]),
    "exa enforcer of the nekroz": ("Creature", "Dragon", [
        "(1 - Déclenchable Hard) **On Sacrifice** — Cherchez 1 Dragon Ritual “Nekroz”.",
        "(2 - Déclenchable Hard) Si cette carte est exilée, renvoyez sur le terrain 1 autre créature “Nekroz” ciblée depuis l’exil.",
    ]),
    "manju of the ten thousand hands": ("Creature", "Fairy", [
        "(1 - Déclenchable) <b>On Enter</b> — Cherchez 1 Ritual Creature ou 1 carte non-créature avec le sous-type Invocation Ritual.",
    ]),
    "senju of the thousand hands": ("Creature", "Fairy", [
        "(1 - Déclenchable) <b>On Enter</b> — Cherchez 1 créature Ritual.",
    ]),
    "herald of the arc light": ("Synchro Creature", "Psychic", [
        "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>",
        "(1 - Passif) Si une carte devait être mise au GY depuis une main ou un Deck, exilez-la à la place.",
        "(2 - Déclenchable) <b>On Send GY</b> — Cherchez 1 Ritual Creature ou 1 carte non-créature avec le sous-type Invocation Ritual.",
    ]),
    "nekroz kaleidoscope": ("Sorcery", "Invocation Ritual", [
        "(1 - Résolution) Mettez en jeu 1 ou plusieurs créatures Ritual “Nekroz” depuis votre main en envoyant 1 créature depuis votre Sideboard au GY comme matériel dont la MV satisfait seule leur(s) coût Ritual.",
        "(2 - Activable Sorcery Hard) <b>Nekroz Recovery</b> — Si vous ne contrôlez aucune créature : exilez cette carte et 1 autre carte “Nekroz” depuis votre GY ; cherchez 1 carte non-créature Invocation Ritual “Nekroz”.",
    ]),
    "nekroz mirror": ("Sorcery", "Invocation Ritual", [
        "(1 - Résolution) Mettez en jeu 1 créature Ritual “Nekroz” depuis votre main en exilant des créatures depuis votre GY ou en sacrifiant des créatures depuis votre main ou terrain dont la MV totale satisfait son coût Ritual.",
        "(2 - Activable Sorcery Hard) <b>Nekroz Recovery</b> — Si vous ne contrôlez aucune créature : exilez cette carte et 1 autre carte “Nekroz” depuis votre GY ; cherchez 1 carte non-créature Invocation Ritual “Nekroz”.",
    ]),
    "nekroz cycle": ("Sorcery", "Invocation Ritual", [
        "(1 - Résolution) Mettez en jeu 1 créature Ritual “Nekroz” depuis votre main ou GY en sacrifiant des créatures depuis votre main ou terrain dont la MV totale satisfait son coût Ritual.",
        "(2 - Activable Sorcery Hard) <b>Nekroz Recovery</b> — Si vous ne contrôlez aucune créature : exilez cette carte et 1 autre carte “Nekroz” depuis votre GY ; cherchez 1 carte non-créature Invocation Ritual “Nekroz”.",
    ]),
}


def update_card(path: Path) -> None:
    key = path.name.removeprefix("card ")
    if key not in CARDS:
        return
    super_type, subtype, rules = CARDS[key]
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"\tsuper_type:.*", f"\tsuper_type: <word-list-type-en>{super_type}</word-list-type-en>", text)
    subtype_list = "word-list-spell" if super_type in {"Sorcery", "Instant", "Enchantment"} else "word-list-race-en"
    subtype_value = f"<{subtype_list}>{subtype}</{subtype_list}>" if subtype else ""
    text = re.sub(r"\tsub_type:.*", f"\tsub_type: {subtype_value}", text)
    block = "\trule_text:\n" + "\n".join(f"\t\t{rule}" for rule in rules) + "\n"
    text = re.sub(r"\trule_text:\n.*?(?=\tflavor_text:)", block, text, flags=re.DOTALL)
    path.write_text("\ufeff" + text.lstrip("\ufeff"), encoding="utf-8")


for project in (PROJECT, SYNCHRO_PROJECT):
    for card_file in project.glob("card *"):
        update_card(card_file)

print(f"Updated {len(CARDS)} Nekroz card templates.")
