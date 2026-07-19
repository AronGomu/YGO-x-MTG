from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects/13_YGO_Spellbook.mse-set"
DOC = ROOT / "docs/13_archetype_spellbook.md"

BOOK_AFFINITY = "<b>Book Affinity</b>"
SPELL_AFFINITY = "<b>Spell Affinity</b>"

EXPECTED_RULES = {
    "card high priestess of prophecy": ("<b>Alternative Cost</b>", "Reveal 3 non-creature “Spellbook” from hand", "Exile 1 “Spellbook” from hand or <b>Grave</b>"),
    "card justice of prophecy": ("<b>On End Step</b>", "If 1 non-creature “Spellbook” was cast this turn", "Search 1 “Spellbook”"),
    "card spellbook library of the crescent": ("If you control 1 Wizard MV 2+", "reveal 3 “Spellbook” from Deck", "Put the chosen card into hand"),
    "card spellbook magician of prophecy": ("<b>Alternative Cost</b>", "If you cast 1 non-creature “Spellbook” this turn", "<b>On Enter</b>", "Search 1 “Spellbook”"),
    "card spellbook of eternity": ("Target 1 “Spellbook” from exile", "<b>Reclaim</b> the target"),
    "card spellbook of fate": ("Exile 1–3 “Spellbook” from <b>Grave</b>", "2 — <b>Bounce</b> 1 nonland permanent", "3 — Exile 1 nonland permanent"),
    "card spellbook of judgment": ("<b>This turn On End Step</b>", "Search 0–(X−2) “Spellbook”", "non-creature “Spellbook” cast this turn", "<b>Summon</b> 1 “Spellbook” creature MV X or less from Deck"),
    "card spellbook of knowledge": ("Sacrifice 1 “Spellbook” or discard 1 “Spellbook”; draw 2 cards",),
    "card spellbook of life": ("Target 1 Wizard creature MV X in <b>Grave</b>", "choose X non-creature “Spellbook” from <b>Grave</b>", "<b>Reanimate</b> it, if you do, exile the chosen cards"),
    "card spellbook of miracles": ("Target 1 Wizard in <b>Grave</b> and 0–2 non-creature “Spellbook” in exile", "<b>Reanimate</b> the Wizard", "<b>Attach</b> the targeted “Spellbook” to it"),
    "card spellbook of power": ("Target 1 “Spellbook”; until end of turn, the target gets +2/+2", "Search 1 “Spellbook”"),
    "card spellbook of secrets": ("Search 1 “Spellbook”",),
    "card spellbook of the master": ("Reveal 1 other “Spellbook” from hand", "target 1 “Spellbook” from <b>Grave</b>", "copy the target's Resolution effect and resolve it"),
    "card spellbook of wisdom": ("it gains <b>Protection from everything</b> until end of turn",),
    "card spellbook star hall": ("<b>On Cast “Spellbook”</b>", "<b>On Leave Field</b>", "Search 1 “Spellbook” creature MV X or less"),
    "card the grand spellbook tower": ("<b>On Upkeep</b>", "put 1 “Spellbook” from <b>Grave</b> on the bottom of Deck", "<b>On Leave Field</b>", "<b>Summon</b> 1 “Spellbook” creature from Deck"),
}

SPELL_AFFINITY_CARDS = {
    "card spellbook library of the crescent",
    "card spellbook of eternity",
    "card spellbook of fate",
    "card spellbook of knowledge",
    "card spellbook of life",
    "card spellbook of miracles",
    "card spellbook of power",
    "card spellbook of secrets",
    "card spellbook of the master",
    "card spellbook of wisdom",
}

RESOLUTION_HARD_CARDS = SPELL_AFFINITY_CARDS - {"card spellbook library of the crescent"} | {
    "card spellbook of judgment"
}


class SpellbookCardTests(unittest.TestCase):
    def test_manifest_is_sorted_complete_and_english(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = re.findall(r"(?m)^include_file:\s*(.+)$", set_text)
        self.assertEqual(includes, sorted(EXPECTED_RULES))
        self.assertEqual(len(includes), 16)
        self.assertIn("title: YGO x MTG -- Spellbook", set_text)
        self.assertIn("set_language: EN", set_text)
        self.assertIn("card_language: English", set_text)

    def test_every_card_uses_current_english_templating(self) -> None:
        stale = re.compile(r"\b(?:library|graveyard|mana value|Magicien|Révélez|cible|cherchez|mettez)\b|error-spelling", re.I)
        for filename, fragments in EXPECTED_RULES.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                rule_text = text.split("\trule_text:\n", 1)[1].split("\tflavor_text:", 1)[0]
                for fragment in fragments:
                    self.assertIn(fragment, rule_text)
                self.assertNotRegex(rule_text, stale)
                self.assertNotIn(BOOK_AFFINITY, rule_text)
                if filename in SPELL_AFFINITY_CARDS:
                    self.assertIn(SPELL_AFFINITY, rule_text)
                else:
                    self.assertNotIn(SPELL_AFFINITY, rule_text)
                if filename in RESOLUTION_HARD_CARDS:
                    self.assertEqual(rule_text.count("(1 - Resolution Hard)"), 1)
                elif filename == "card spellbook library of the crescent":
                    self.assertEqual(rule_text.count("(1 - Resolution)"), 1)

    def test_types_and_subtypes_are_english(self) -> None:
        for filename in (
            "card high priestess of prophecy",
            "card justice of prophecy",
            "card spellbook magician of prophecy",
        ):
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            subtype = next(line.removeprefix("\tsub_type: ") for line in text.splitlines() if line.startswith("\tsub_type: "))
            self.assertEqual(" ".join(re.sub(r"<[^>]+>", "", subtype).split()), "Wizard Spellbook")
        tower = (PROJECT / "card the grand spellbook tower").read_text(encoding="utf-8-sig")
        subtype = next(line.removeprefix("\tsub_type: ") for line in tower.splitlines() if line.startswith("\tsub_type: "))
        self.assertEqual(" ".join(re.sub(r"<[^>]+>", "", subtype).split()), "Land")

    def test_archetype_doc_keeps_affinity_rules_not_card_blocks(self) -> None:
        doc = DOC.read_text(encoding="utf-8-sig")
        self.assertIn("**Book Affinity** is retired", doc)
        self.assertIn("**Alternative Cost**", doc)
        self.assertIn("**Spell Affinity**", doc)
        self.assertIn("printed, opt-in keyword", doc)
        self.assertIn("## Card source of truth", doc)
        self.assertIn("MSE_projects/13_YGO_Spellbook.mse-set", doc)
        self.assertNotIn("\nCreature — Wizard Spellbook\n", doc)

    def test_retired_generator_cannot_overwrite_canonical_project(self) -> None:
        generator = (ROOT / ".script/create_archetype_projects.py").read_text(encoding="utf-8-sig")
        self.assertIn("Retired", generator)
        self.assertIn("English folder-form projects", generator)
        self.assertNotIn("shutil.rmtree", generator)
        self.assertFalse((ROOT / "mse/set").exists())
        self.assertTrue((ROOT / "mse/French/set").is_file())

    def test_all_images_resolve(self) -> None:
        for filename in EXPECTED_RULES:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image = next(line.split(": ", 1)[1] for line in text.splitlines() if line.startswith("\timage: "))
            self.assertTrue((PROJECT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
