#!/usr/bin/env python3
"""Create generic Extra Deck staple MSE projects with imported root images."""

from __future__ import annotations

import json
import re
import time
import unicodedata
from pathlib import Path
from datetime import datetime

import requests
from PIL import Image, ImageOps

from original_image_assets import original_image_path

REPO = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO / "MSE_projects"
DOC = REPO / "09_non_archetype_non_creature.md"
API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

PROJECTS = {
    "Fusion": ("YGO_Staples_Fusion.mse-set", "YGO x MTG -- Staples Fusion", "YSF", "Fusion Creature"),
    "Synchro": ("YGO_Staples_Synchro.mse-set", "YGO x MTG -- Staples Synchro", "YSS", "Synchro Creature"),
    "Xyz": ("YGO_Staples_Xyz.mse-set", "YGO x MTG -- Staples Xyz", "YSX", "Xyz Creature"),
    "Link": ("YGO_Staples_Link.mse-set", "YGO x MTG -- Staples Link", "YSL", "Link Creature"),
}

CARDS = {
    "Fusion": [
        ("Mudragon of the Swamp", "<i>Fusion — 2 créatures avec le même attribut mais des types différents</i>", ["(1 - Passif) Les créatures que vous contrôlez avec un attribut choisi ont ward 2.", "(2 - Activable Flash Soft) Choisissez un attribut ; Mudragon devient de cet attribut jusqu'à la fin du tour."]),
        ("Garura, Wings of Resonant Life", "<i>Fusion — 2 créatures avec le même type et attribut mais des noms différents</i>", ["(1 - Passif) Vol.", "(2 - Déclenchable) <b>On Send GY</b> — Piochez une carte."]),
        ("Elder Entity N'tss", "<i>Fusion — 1 Synchro Creature + 1 Xyz Creature</i>", ["(1 - Déclenchable) Si Elder Entity N'tss arrive, vous pouvez mettre une créature depuis votre extra deck dans votre cimetière.", "(2 - Déclenchable) <b>On Send GY</b> — Détruisez le permanent ciblé."]),
        ("Starving Venom Fusion Dragon", "<i>Fusion — 2 créatures DARK</i>", ["(1 - Déclenchable) Si Starving Venom arrive, il gagne +X/+0 jusqu'à la fin du tour, où X est la force d'une créature adverse ciblée.", "(2 - Déclenchable) Si Starving Venom meurt, détruisez toutes les créatures adverses qui ont des marqueurs."]),
        ("Predaplant Dragostapelia", "<i>Fusion — 1 Fusion Creature + 1 créature DARK</i>", ["(1 - Activable Flash Soft) Mettez un marqueur Predator sur une créature ciblée.", "(2 - Passif) Les créatures adverses avec un marqueur Predator perdent toutes leurs capacités activées."]),
        ("Millennium-Eyes Restrict", "<i>Fusion — 1 créature Effect + 1 créature Restrict</i>", ["(1 - Déclenchable Soft) Si un adversaire active une capacité de créature, exilez cette créature jusqu'à ce que Millennium-Eyes quitte le champ de bataille.", "(2 - Passif) Les cartes avec le même nom qu'une carte exilée par Millennium-Eyes ne peuvent pas activer leurs capacités."]),
        ("Thousand-Eyes Restrict", "<i>Fusion — 1 créature Restrict + 1 créature Illusionist</i>", ["(1 - Déclenchable) Si Thousand-Eyes arrive, exilez une autre créature ciblée jusqu'à ce qu'il quitte le champ de bataille.", "(2 - Passif) Les autres créatures ne peuvent pas attaquer."]),
        ("Sea Monster of Theseus", "<i>Fusion — 2 créatures Tuner</i>", ["(1 - Passif) Cette carte compte comme 2 matériaux pour une invocation Synchro."]),
        ("Panzer Dragon", "<i>Fusion — 1 Machine + 1 Dragon</i>", ["(1 - Passif) Vol.", "(2 - Déclenchable) Si Panzer Dragon meurt, détruisez le permanent ciblé."]),
        ("Mysterion the Dragon Crown", "<i>Fusion — 1 Wizard + 1 Dragon</i>", ["(1 - Déclenchable Soft) Si votre adversaire active une capacité d'une créature, exilez cette créature.", "(2 - Passif) Mysterion gagne -1/-0 pour chaque carte exilée par lui."]),
        ("Dragonecro Nethersoul Dragon", "<i>Fusion — 2 créatures Zombie</i>", ["(1 - Passif) Si Dragonecro combat une créature, cette créature devient 0/1 jusqu'à la fin du tour.", "(2 - Déclenchable) Si Dragonecro inflige des blessures de combat, créez un jeton Zombie noir X/X, où X est la force de la créature blessée."]),
        ("World Chalice Guardragon Almarduke", "<i>Fusion — 3 Link Creatures</i>", ["(1 - Passif) Peut attaquer toutes les créatures adverses une fois chacune.", "(2 - Déclenchable) Si Almarduke détruit une créature au combat, il inflige 2 blessures à son contrôleur."]),
        ("Earth Golem @Ignister", "<i>Fusion — 1 Cyberse + 1 Link Creature</i>", ["(1 - Déclenchable) Si Earth Golem arrive, prévenez les prochaines blessures que les Link Creatures vous infligeraient ce tour-ci.", "(2 - Déclenchable) Si Earth Golem détruit une créature au combat, il inflige 2 blessures à son contrôleur."]),
        ("Salamangreat Violet Chimera", "<i>Fusion — 1 Salamangreat + 1 Link Creature</i>", ["(1 - Déclenchable) Si Violet Chimera arrive, elle gagne +X/+0 jusqu'à la fin du tour, où X est la force d'une créature ciblée dans un cimetière.", "(2 - Déclenchable) Si Violet Chimera combat une créature affaiblie, doublez sa force jusqu'à la fin du tour."]),
        ("Coordius the Triphasic Dealmon", "<i>Fusion — 1 Synchro + 1 Xyz + 1 Link</i>", ["(1 - Déclenchable) Si Coordius arrive, vous pouvez payer 6 points de vie. Si vous faites ainsi, piochez une carte, détruisez une carte ciblée et renvoyez une carte ciblée depuis votre cimetière dans votre main.", "(2 - Passif) À chaque fois que vous payez des points de vie, Coordius gagne +1/+1 jusqu'à la fin du tour."]),
    ],
    "Synchro": [
        ("Baronne de Fleur", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Activable Sorcery Soft) Détruisez une carte ciblée.", "(2 - Activable Flash Hard) Contrecarrez un sort ou une capacité ciblé, puis détruisez-le."]),
        ("Borreload Savage Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Déclenchable) Si Borreload arrive, exilez une Link Creature de votre cimetière. Mettez X marqueurs Borrel sur Borreload, où X est son Link.", "(2 - Activable Flash) Retirez un marqueur Borrel : contrecarrez un sort ou une capacité ciblé."]),
        ("Chaos Angel", "<i>Synchro — 1 Tuner + 1+ non-Tuner LIGHT ou DARK</i>", ["(1 - Déclenchable) Si Chaos Angel arrive, exilez une carte ciblée sur le champ de bataille.", "(2 - Passif) Si Chaos Angel a été invoqué avec une créature LIGHT et une créature DARK, il a vigilance et indestructible."]),
        ("Swordsoul Supreme Sovereign - Chengying", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Passif) Chengying gagne +1/+1 pour chaque carte exilée et les créatures adverses gagnent -1/-1 pour chaque carte exilée par vous ce tour-ci.", "(2 - Déclenchable Soft) Si une carte est exilée, exilez une carte ciblée sur le champ de bataille et une carte ciblée d'un cimetière."]),
        ("PSY-Framelord Omega", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Activable Flash Soft) Exilez Omega et une carte aléatoire de la main d'un adversaire jusqu'au début de votre prochain entretien.", "(2 - Activable Sorcery Soft) Remettez une carte exilée dans le cimetière de son propriétaire."]),
        ("Crystal Wing Synchro Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner Synchro</i>", ["(1 - Activable Flash Soft) Contrecarrez la capacité d'une créature ciblée, détruisez cette créature, puis Crystal Wing gagne sa force jusqu'à la fin du tour.", "(2 - Déclenchable) Si Crystal Wing combat une créature de force 3 ou plus, il gagne +2/+0 jusqu'à la fin du tour."]),
        ("Accel Synchro Stardust Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Déclenchable) Si Accel Synchro arrive, renvoyez une créature Tuner ciblée depuis votre cimetière sur le champ de bataille.", "(2 - Activable Flash Soft) Exilez Accel Synchro : invoquez une Synchro Creature depuis votre extra deck en utilisant vos créatures comme matériaux."]),
        ("Stardust Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Activable Flash Soft) Sacrifiez Stardust Dragon : contrecarrez un sort ou une capacité qui détruirait une carte sur le champ de bataille.", "(2 - Déclenchable) Au début de la prochaine étape de fin, renvoyez Stardust Dragon depuis votre cimetière sur le champ de bataille."]),
        ("Black Rose Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Déclenchable) Si Black Rose arrive, vous pouvez détruire toutes les cartes non-terrain.", "(2 - Activable Sorcery Soft) Exilez une créature Plant de votre cimetière : une créature ciblée ne peut pas bloquer ce tour-ci."]),
        ("Trishula, Dragon of the Ice Barrier", "<i>Synchro — 1 Tuner + 2+ non-Tuner</i>", ["(1 - Déclenchable) Si Trishula arrive, exilez jusqu'à une carte ciblée depuis la main, le champ de bataille et le cimetière d'un adversaire."]),
        ("Brionac, Dragon of the Ice Barrier", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Activable Sorcery Soft) Défaussez-vous d'un nombre de cartes ; renvoyez autant de permanents ciblés dans la main de leurs propriétaires."]),
        ("Coral Dragon", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Activable Sorcery Soft) Défaussez-vous d'une carte : détruisez une carte ciblée.", "(2 - Déclenchable) <b>On Send GY</b> — Piochez une carte."]),
        ("Formula Synchron", "<i>Synchro — 1 Tuner + 1 non-Tuner</i>", ["(1 - Déclenchable) Si Formula Synchron arrive, piochez une carte.", "(2 - Activable Flash Soft) Invoquez une Synchro Creature depuis votre extra deck en utilisant vos créatures comme matériaux."]),
        ("Herald of the Arc Light", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Passif) Si une carte devait être mise dans un cimetière depuis une main ou une bibliothèque, exilez-la à la place.", "(2 - Déclenchable) <b>On Send GY</b> — Cherchez une créature Ritual ou une carte Ritual."]),
        ("T.G. Hyper Librarian", "<i>Synchro — 1 Tuner + 1+ non-Tuner</i>", ["(1 - Déclenchable Soft) À chaque fois qu'une Synchro Creature arrive sous votre contrôle, piochez une carte."]),
    ],
    "Xyz": [
        ("Abyss Dweller", "<i>Xyz 2</i>", ["(1 - Activable Flash Soft) Détachez un matériau : les cartes dans les cimetières adverses perdent toutes leurs capacités jusqu'à la fin du tour.", "(2 - Passif) Si Abyss Dweller a un matériau WATER, les créatures que vous contrôlez gagnent +1/+0."]),
        ("Number 41: Bagooska the Terribly Tired Tapir", "<i>Xyz 2</i>", ["(1 - Passif) Les créatures dégagées adverses ne peuvent pas attaquer.", "(2 - Passif) Les créatures engagées adverses perdent toutes leurs capacités."]),
        ("Tornado Dragon", "<i>Xyz 2</i>", ["(1 - Activable Flash Soft) Détachez un matériau : détruisez un permanent non-créature non-terrain ciblé."]),
        ("Divine Arsenal AA-ZEUS - Sky Thunder", "<i>Xyz — 1 Xyz Creature qui a combattu ce tour-ci</i>", ["(1 - Activable Flash) Détachez deux matériaux : mettez toutes les autres cartes non-terrain dans les cimetières de leurs propriétaires.", "(2 - Déclenchable Soft) Si une autre carte que vous contrôlez est détruite, attachez une carte de votre main, champ de bataille ou extra deck à ZEUS comme matériau."]),
        ("Number 38: Hope Harbinger Dragon Titanic Galaxy", "<i>Xyz 2</i>", ["(1 - Activable Flash Soft) Contrecarrez un sort non-créature ciblé et attachez-le à Hope Harbinger comme matériau.", "(2 - Activable Flash Soft) Redirigez une attaque vers Hope Harbinger."]),
        ("Number 60: Dugares the Timeless", "<i>Xyz 2</i>", ["(1 - Activable Sorcery Soft) Détachez deux matériaux et choisissez un mode : piochez deux puis défaussez une carte ; renvoyez une créature depuis votre cimetière ; ou doublez la force d'une créature jusqu'à la fin du tour. Sautez votre prochaine étape associée."]),
        ("Evilswarm Exciton Knight", "<i>Xyz 2</i>", ["(1 - Activable Flash Soft) Si un adversaire a plus de cartes que vous, détachez un matériau : détruisez toutes les autres cartes non-terrain."]),
        ("Time Thief Redoer", "<i>Xyz 2</i>", ["(1 - Déclenchable) Au début de chaque entretien, attachez la carte du dessus de la bibliothèque d'un adversaire à Redoer comme matériau.", "(2 - Activable Flash Soft) Détachez des matériaux pour exiler Redoer jusqu'à la fin du tour, piocher une carte, ou renvoyer une carte ciblée au-dessus de la bibliothèque."]),
        ("Number 101: Silent Honor ARK", "<i>Xyz 2</i>", ["(1 - Activable Sorcery Soft) Détachez deux matériaux : exilez une créature attaquante ciblée jusqu'à ce que Silent Honor quitte le champ de bataille.", "(2 - Passif) Si Silent Honor devait être détruit, détachez un matériau à la place."]),
        ("Super Starslayer TY-PHON - Sky Crisis", "<i>Xyz — 1 Xyz Creature ou 2 créatures</i>", ["(1 - Passif) Tant que TY-PHON est sur le champ de bataille, les créatures avec une force de 3 ou plus ne peuvent pas activer leurs capacités.", "(2 - Activable Sorcery Soft) Détachez un matériau : renvoyez une créature ciblée dans la main de son propriétaire."]),
        ("The Phantom Knights of Break Sword", "<i>Xyz 2</i>", ["(1 - Activable Sorcery Soft) Détachez un matériau : détruisez une carte que vous contrôlez et une carte qu'un adversaire contrôle.", "(2 - Déclenchable) Si Break Sword est détruit, renvoyez jusqu'à deux créatures DARK depuis votre cimetière engagées."]),
        ("Dingirsu, the Orcust of the Evening Star", "<i>Xyz 2</i>", ["(1 - Déclenchable) Si Dingirsu arrive, choisissez : exilez une carte ciblée qu'un adversaire contrôle, ou attachez une carte exilée à Dingirsu comme matériau.", "(2 - Passif) Si une carte que vous contrôlez devait être détruite, détachez un matériau à la place."]),
        ("Number 90: Galaxy-Eyes Photon Lord", "<i>Xyz 2</i>", ["(1 - Activable Flash Soft) Détachez un matériau : contrecarrez une capacité de créature ciblée. Si le matériau était LIGHT, détruisez cette créature.", "(2 - Déclenchable Soft) Pendant l'étape de fin adverse, cherchez une créature LIGHT."]),
        ("Number 11: Big Eye", "<i>Xyz 2</i>", ["(1 - Activable Sorcery Soft) Détachez un matériau : acquérez le contrôle de la créature ciblée tant que vous contrôlez Big Eye. Big Eye ne peut pas attaquer ce tour-ci."]),
        ("Number 4: Stealth Kragen", "<i>Xyz 2</i>", ["(1 - Passif) Toutes les créatures sur le champ de bataille sont WATER en plus de leurs autres attributs.", "(2 - Activable Flash Soft) Détruisez une créature WATER ciblée et infligez 2 blessures à son contrôleur."]),
    ],
    "Link": [
        ("S:P Little Knight", "<i>Link 2</i>", ["(1 - Déclenchable) Si S:P arrive, si elle a utilisé une Extra Deck Creature comme matériau, exilez une carte ciblée sur le champ de bataille jusqu'à votre prochaine étape de fin.", "(2 - Activable Flash Soft) Si un adversaire active un effet, exilez S:P et une créature ciblée jusqu'à la fin du tour."]),
        ("I:P Masquerena", "<i>Link 2</i>", ["(1 - Activable Flash Soft) Invoquez une Link Creature depuis votre extra deck en utilisant vos créatures comme matériaux.", "(2 - Passif) Une Link Creature invoquée avec I:P comme matériau a indestructible contre les effets de carte."]),
        ("Apollousa, Bow of the Goddess", "<i>Link 2+</i>", ["(1 - Passif) Apollousa arrive avec X marqueurs Force, où X est le nombre de matériaux utilisés.", "(2 - Activable Flash) Retirez un marqueur Force : contrecarrez une capacité de créature ciblée."]),
        ("Accesscode Talker", "<i>Link 2+</i>", ["(1 - Déclenchable) Si Accesscode arrive, il gagne +X/+0 jusqu'à la fin du tour, où X est le Link d'une Link Creature ciblée dans votre cimetière.", "(2 - Activable Sorcery) Exilez une Link Creature de votre cimetière : détruisez une carte ciblée. N'activez cette capacité qu'une fois pour chaque attribut par tour."]),
        ("Knightmare Unicorn", "<i>Link 3</i>", ["(1 - Déclenchable) Si Unicorn arrive, vous pouvez vous défausser d'une carte. Si vous faites ainsi, mélangez une carte ciblée dans la bibliothèque de son propriétaire, puis piochez une carte si Unicorn est co-liée."]),
        ("Knightmare Phoenix", "<i>Link 2</i>", ["(1 - Déclenchable) Si Phoenix arrive, vous pouvez vous défausser d'une carte. Si vous faites ainsi, détruisez un permanent non-créature non-terrain ciblé, puis piochez une carte si Phoenix est co-liée."]),
        ("Knightmare Cerberus", "<i>Link 2</i>", ["(1 - Déclenchable) Si Cerberus arrive, vous pouvez vous défausser d'une carte. Si vous faites ainsi, détruisez une créature ciblée, puis piochez une carte si Cerberus est co-liée."]),
        ("Linkuriboh", "<i>Link 1</i>", ["(1 - Activable Flash Soft) Sacrifiez Linkuriboh : une créature attaquante ciblée devient 0/1 jusqu'à la fin du tour.", "(2 - Activable Sorcery Soft) Sacrifiez une créature de valeur de mana 1 : renvoyez Linkuriboh depuis votre cimetière sur le champ de bataille."]),
        ("Relinquished Anima", "<i>Link 1</i>", ["(1 - Activable Sorcery Soft) Exilez une créature ciblée qu'un adversaire contrôle jusqu'à ce qu'Anima quitte le champ de bataille.", "(2 - Passif) Anima gagne +X/+0, où X est la force de la carte exilée par lui."]),
        ("Salamangreat Almiraj", "<i>Link 1</i>", ["(1 - Activable Flash Soft) Sacrifiez Almiraj : une créature ciblée que vous contrôlez gagne indestructible jusqu'à la fin du tour.", "(2 - Activable Sorcery Soft) Si une créature que vous contrôliez a été détruite ce tour-ci, renvoyez Almiraj depuis votre cimetière sur le champ de bataille."]),
        ("Cross-Sheep", "<i>Link 2</i>", ["(1 - Déclenchable Soft) Si une Extra Deck Creature arrive dans une zone pointée par Cross-Sheep, appliquez selon son type : Fusion — renvoyez une créature depuis votre cimetière ; Synchro — les créatures que vous contrôlez gagnent +1/+1 ; Xyz — les créatures adverses gagnent -1/-1."]),
        ("Underworld Goddess of the Closed World", "<i>Link 5</i>", ["(1 - Passif) Vous pouvez utiliser une créature adverse comme matériau pour invoquer Underworld Goddess.", "(2 - Déclenchable) Si Underworld Goddess arrive, les créatures adverses perdent toutes leurs capacités jusqu'à la fin du tour.", "(3 - Activable Flash Soft) Contrecarrez une capacité qui cible une carte dans un cimetière."]),
        ("Mekk-Knight Crusadia Avramax", "<i>Link 4</i>", ["(1 - Passif) Les adversaires ne peuvent pas cibler les autres cartes que vous contrôlez avec des attaques.", "(2 - Déclenchable) Si Avramax combat une créature invoquée spécialement, il gagne +X/+0 jusqu'à la fin du tour, où X est la force de cette créature.", "(3 - Déclenchable) Si Avramax quitte le champ de bataille, mélangez une carte ciblée dans la bibliothèque de son propriétaire."]),
        ("Borrelsword Dragon", "<i>Link 4</i>", ["(1 - Passif) Borrelsword ne peut pas être détruit au combat.", "(2 - Activable Flash Soft) Une créature ciblée ne peut pas attaquer ce tour-ci ; Borrelsword peut attaquer une fois supplémentaire ce tour-ci.", "(3 - Déclenchable) Si Borrelsword attaque une créature, il gagne +X/+0 et cette créature gagne -X/-0 jusqu'à la fin du tour, où X est la moitié de sa force."]),
        ("Topologic Zeroboros", "<i>Link 4</i>", ["(1 - Passif) Zeroboros gagne +1/+1 pour chaque carte exilée.", "(2 - Déclenchable Soft) Si une créature arrive dans une zone pointée par une Link Creature, exilez toutes les cartes sur le champ de bataille.", "(3 - Déclenchable) Au prochain entretien, renvoyez Zeroboros exilé par lui-même sur le champ de bataille."]),
    ],
}

ATTRIBUTE_COST = {"DARK": "B", "LIGHT": "W", "FIRE": "R", "WATER": "U", "EARTH": "G", "WIND": "G", "DIVINE": "W"}


def slug(text: str) -> str:
    text = text.lower().replace("&", "and")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text


def include_name(name: str) -> str:
    return "card " + slug(name).replace("_", " ")


def fetch_card(name: str) -> dict:
    for params in ({"name": name}, {"fname": name}):
        response = requests.get(API, params=params, timeout=40)
        response.raise_for_status()
        data = response.json().get("data", [])
        if data:
            exact = [card for card in data if card["name"].lower() == name.lower()]
            return (exact[0] if exact else data[0])
    raise RuntimeError(f"Card not found: {name}")


def resize_cover(source: Path, output: Path, width: int = 316, height: int = 231) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        sw, sh = image.size
        scale = max(width / sw, height / sh)
        resized = image.resize((round(sw * scale), round(sh * scale)), Image.Resampling.LANCZOS)
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        resized.crop((left, top, left + width, top + height)).save(output, "PNG")


def rich_subtype(race: str) -> str:
    return f"<word-list-race-en>{race}</word-list-race-en>" if race else ""


def stats(card: dict, kind: str) -> tuple[int, int]:
    atk = int(card.get("atk") or 0)
    if kind == "Link":
        link = int(card.get("linkval") or 1)
        return max(1, round(atk / 1000)), max(2, link + 2)
    defense = int(card.get("def") or 1000)
    return max(0, round(atk / 1000)), max(1, round(defense / 1000))


def emit_project(kind: str) -> list[dict]:
    dirname, title, code, super_type = PROJECTS[kind]
    project = OUT_ROOT / dirname
    if project.exists():
        import shutil
        shutil.rmtree(project)
    project.mkdir(parents=True)
    mse_image_dir = project / "mse_images"
    mse_image_dir.mkdir(parents=True)
    cards_out = []
    fetched = []
    for requested, material, rules in CARDS[kind]:
        card = fetch_card(requested)
        fetched.append((requested, material, rules, card))
        time.sleep(0.08)
    fetched.sort(key=lambda item: item[3]["name"].lower())

    includes = []
    for index, (requested, material, rules, card) in enumerate(fetched, start=1):
        name = card["name"]
        inc = include_name(name)
        includes.append(inc)
        src_jpg = original_image_path(card)
        image_url = card["card_images"][0].get("image_url_cropped") or card["card_images"][0].get("image_url")
        if not src_jpg.exists():
            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            src_jpg.parent.mkdir(parents=True, exist_ok=True)
            src_jpg.write_bytes(img_response.content)
        mse_png = mse_image_dir / f"image{index}.png"
        resize_cover(src_jpg, mse_png)
        power, toughness = stats(card, kind)
        cost = ATTRIBUTE_COST.get(card.get("attribute"), "C")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "mse_version: 2.5.8",
            "card:",
            "\thas_styling: false",
            "\tnotes: Source: 09_non_archetype_non_creature.md",
            f"\ttime_created: {now}",
            f"\ttime_modified: {now}",
            f"\tname: {name}",
            f"\tcasting_cost: {cost}",
            f"\timage: {mse_png.relative_to(project).as_posix()}",
            "\timage_2: ",
            "\tmainframe_image: ",
            "\tmainframe_image_2: ",
            f"\tsuper_type: <word-list-type-en>{super_type}</word-list-type-en>",
            f"\tsub_type: {rich_subtype(card.get('race', ''))}",
            "\trarity: rare",
            "\trule_text:",
            f"\t\t{material}",
        ]
        lines += [f"\t\t{line}" for line in rules]
        lines += [
            "\tflavor_text: <i-flavor></i-flavor>",
            f"\tpower: {power}",
            f"\ttoughness: {toughness}",
            f"\tcard_code_text: {index:03d}/{len(fetched):03d} R",
        ]
        (project / inc).write_text("\n".join(lines) + "\n", encoding="utf-8")
        cards_out.append({"name": name, "kind": kind, "race": card.get("race", ""), "cost": cost, "power": power, "toughness": toughness, "material": material, "rules": rules})

    stylesheet_by_supertype = {
        "Fusion": ("genevensis-00-main", "2022-02-22"),
        "Xyz": ("m15-spellbook", "2024-09-01"),
        "Synchro": ("m15-sketch", "2024-09-01"),
        "Link": ("m15-showcase-capenna-art-deco", "2024-10-01"),
        "Ritual": ("m15-showcase-praetor", "2024-09-01"),
    }
    stylesheet, stylesheet_version = stylesheet_by_supertype.get(kind, ("sevenhalf", "2024-05-30"))
    set_lines = [
        "\ufeffmse_version: 2.0.2",
        "game: magic",
        "game_version: 2025-06-14",
        f"stylesheet: {stylesheet}",
        f"stylesheet_version: {stylesheet_version}",
        "set_info:",
        f"\ttitle: {title}",
        "\tdescription: Staples génériques Extra Deck populaires dans l'histoire compétitive de Yu-Gi-Oh, adaptés pour le cube.",
        "\tartist: ",
        "\tcopyright: Fan-made custom cards for private cube playtesting",
        f"\tset_code: {code}",
        "\tset_language: FR",
        "\tsymbol: ",
        "\tmasterpiece_symbol: ",
        "\tcard_language: French",
        "\tautomatic_reminder_text: ",
        "\tautomatic_copyright: yes",
        "\tautomatic_card_numbers: yes",
        "styling:",
        "\tmagic-m15:",
        "\t\ttext_box_mana_symbols: magic-mana-small.mse-symbol-font",
        "\t\toverlay: ",
    ]
    set_lines += [f"include_file: {inc}" for inc in includes]
    set_lines += ["version_control:", "\ttype: none", "apprentice_code: "]
    (project / "set").write_text("\n".join(set_lines) + "\n", encoding="utf-8")
    print(f"{project}: {len(includes)} cards")
    return cards_out


def update_doc(all_cards: dict[str, list[dict]]) -> None:
    text = DOC.read_text(encoding="utf-8-sig")
    start = "\n## Extra Deck générique — projets MSE générés\n"
    if start in text:
        text = text.split(start)[0].rstrip() + "\n"
    out = [text.rstrip(), start.strip(), "", "Ces sections listent les staples génériques sélectionnées pour les nouveaux projets MSE Fusion, Synchro, Xyz et Link. Les effets sont des adaptations cube jouables, pas des traductions littérales.", ""]
    type_line = {"Fusion": "Fusion Creature", "Synchro": "Synchro Creature", "Xyz": "Xyz Creature", "Link": "Link Creature"}
    for kind, cards in all_cards.items():
        out += [f"### Staples {kind}", ""]
        for card in cards:
            material_doc = card["material"].replace("<i>", "*").replace("</i>", "*")
            out += [
                f"#### {card['name']} => {card['name']}", "",
                f"**Coût :** {{{card['cost']}}}", "",
                f"{type_line[kind]} — {card['race']}", "",
                f"**{card['power']} / {card['toughness']}**", "",
                material_doc, "",
            ]
            for rule in card["rules"]:
                out.append(rule.replace("<b>", "**").replace("</b>", "**"))
                out.append("")
            out.append("---")
            out.append("")
    DOC.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    all_cards = {}
    for kind in ("Fusion", "Synchro", "Xyz", "Link"):
        all_cards[kind] = emit_project(kind)
    update_doc(all_cards)


if __name__ == "__main__":
    main()
