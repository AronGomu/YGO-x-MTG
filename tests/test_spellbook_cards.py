from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "13_YGO_Spellbook.mse-set"
DOC = ROOT / "docs" / "13_archetype_spellbook.md"
AGGREGATE = ROOT / "mse" / "set"

BOOK_AFFINITY = "<b>Book Affinity</b>"
SPELL_AFFINITY = "<b>Spell Affinity</b>"

EXPECTED_RULES = {
    "card high priestess of prophecy": (
        BOOK_AFFINITY,
        "<b>Coût alternatif</b> — Révélez 3 “Spellbook” non-creature de votre main.",
        "(1 - Activable Hard)</i-auto> Exilez 1 “Spellbook” de votre main ou Grave",
    ),
    "card justice of prophecy": (
        BOOK_AFFINITY,
        "(1 - Déclenchable Hard)</i-auto> <b>On Enter</b> —",
        "cherchez 1 “Spellbook”",
    ),
    "card spellbook library of the crescent": (
        "(1 - Résolution)</i-auto> Si vous contrôlez 1 Wizard MV 2+",
        "révélez 3 “Spellbook” de votre Deck",
        "Mettez-le dans votre main",
    ),
    "card spellbook magician of prophecy": (
        BOOK_AFFINITY,
        "(1 - Déclenchable Hard)</i-auto> <b>On Enter</b> — Cherchez 1 “Spellbook”.",
    ),
    "card spellbook of eternity": (
        "(1 - Résolution)</i-auto> Ciblez 1 “Spellbook” depuis votre exil ; <b>Reclaim</b> la cible.",
    ),
    "card spellbook of fate": (
        "(1 - Résolution)</i-auto> Exilez jusqu’à 3 “Spellbook” de votre Grave",
        "3 — Exilez 1 permanent.",
    ),
    "card spellbook of judgment": (
        "<b>On Your Cast “Spellbook”</b>",
        "cherchez jusqu’à X “Spellbook”",
        "mettre en jeu depuis votre Deck 1 créature “Spellbook” MV X ou moins",
    ),
    "card spellbook of knowledge": (
        "défaussez 1 “Spellbook”",
        "(1 - Résolution)</i-auto> Piochez 2 cartes.",
    ),
    "card spellbook of life": (
        "Ciblez 1 créature “Spellbook” et X “Spellbook” non-creature de votre Grave",
        "<b>Reanimate</b> la cible si X égale la MV de la cible.",
    ),
    "card spellbook of miracles": (
        "Ciblez 1 Wizard de votre Grave et jusqu’à 2 “Spellbook” non-creature en exil",
        "<b>Reanimate</b> la cible",
        "<b>Attach</b> les “Spellbook” non-creature ciblés",
        "Sinon, ils restent en exil.",
    ),
    "card spellbook of power": (
        "Ciblez 1 “Spellbook” ; la cible gagne +2/+2",
        "cherchez 1 “Spellbook”",
    ),
    "card spellbook of secrets": (
        "(1 - Résolution)</i-auto> Cherchez 1 “Spellbook”.",
    ),
    "card spellbook of the master": (
        "Révélez 1 autre “Spellbook” de votre main",
        "choisissez 1 “Spellbook” dans votre Grave",
        "copiez son texte et résolvez-le",
    ),
    "card spellbook of wisdom": (
        "Ciblez 1 créature “Spellbook” ; elle gagne la protection contre les sorts et les permanents non-créature",
    ),
    "card spellbook star hall": (
        "(1 - Déclenchable)</i-auto> <b>On Your Cast “Spellbook”</b> —",
        "<b>On Leave Field</b>",
        "chercher 1 créature “Spellbook” MV X ou moins",
    ),
    "card the grand spellbook tower": (
        "(1 - Déclenchable Soft)</i-auto> <b>On Upkeep</b>",
        "mettre 1 “Spellbook” depuis votre Grave",
        "<b>On Leave Field</b>",
        "mettre en jeu depuis votre Deck 1 créature “Spellbook”",
    ),
}

SORCERIES = {
    filename
    for filename in EXPECTED_RULES
    if filename
    not in {
        "card high priestess of prophecy",
        "card justice of prophecy",
        "card spellbook magician of prophecy",
        "card spellbook star hall",
        "card the grand spellbook tower",
    }
}


class SpellbookCardTests(unittest.TestCase):
    def test_manifest_is_sorted_complete_and_uses_current_title(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = re.findall(r"(?m)^include_file:\s*(.+)$", set_text)
        self.assertEqual(includes, sorted(EXPECTED_RULES))
        self.assertEqual(len(includes), 16)
        self.assertIn("\ttitle: YGO x MTG -- Spellbook", set_text)

    def test_every_card_uses_current_french_templating(self) -> None:
        stale_terms = (
            "bibliothèque",
            "cimetière",
            "valeur de mana",
            "trois cartes",
            "deux cartes",
            "Magicien",
            "Vous ne pouvez activer cette capacité",
        )
        for filename, fragments in EXPECTED_RULES.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                rule_text = text.split("\trule_text:\n", 1)[1].split(
                    "\tflavor_text:", 1
                )[0]
                for fragment in fragments:
                    self.assertIn(fragment, rule_text)
                for stale in stale_terms:
                    self.assertNotIn(stale, rule_text)
                self.assertNotIn("error-spelling", rule_text)
                self.assertNotRegex(
                    rule_text,
                    r"\bcartes?(?: de créature)? “Spellbook”",
                )
                if filename in SORCERIES:
                    self.assertIn(SPELL_AFFINITY, rule_text)
                    self.assertEqual(rule_text.count("(1 - Résolution)"), 1)

    def test_types_and_subtypes_are_english(self) -> None:
        for filename in (
            "card high priestess of prophecy",
            "card justice of prophecy",
            "card spellbook magician of prophecy",
        ):
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            subtype = next(
                line.removeprefix("\tsub_type: ")
                for line in text.splitlines()
                if line.startswith("\tsub_type: ")
            )
            self.assertEqual(
                " ".join(re.sub(r"<[^>]+>", "", subtype).split()),
                "Wizard Spellbook",
            )
        tower = (PROJECT / "card the grand spellbook tower").read_text(
            encoding="utf-8-sig"
        )
        tower_subtype = next(
            line.removeprefix("\tsub_type: ")
            for line in tower.splitlines()
            if line.startswith("\tsub_type: ")
        )
        self.assertEqual(
            " ".join(re.sub(r"<[^>]+>", "", tower_subtype).split()),
            "Land",
        )

    def test_archetype_doc_keeps_affinity_rules_not_card_blocks(self) -> None:
        doc = DOC.read_text(encoding="utf-8-sig")
        self.assertIn("**Book Affinity**", doc)
        self.assertIn("**Spell Affinity**", doc)
        self.assertIn("Source de vérité des cartes", doc)
        self.assertIn("MSE_projects/13_YGO_Spellbook.mse-set", doc)
        self.assertNotIn("\nCreature — Wizard Spellbook\n", doc)
        self.assertNotRegex(doc, r"(?m)^### .+ => .+")

    def test_generator_targets_canonical_project_and_preserves_art(self) -> None:
        generator = (ROOT / ".script" / "create_archetype_projects.py").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("13_YGO_Spellbook.mse-set", generator)
        self.assertIn("09_YGO_Non_Archetype_Non_Creatures.mse-set", generator)
        self.assertIn("existing_field('image')", generator)
        self.assertIn("'Book Affinity'", generator)
        self.assertIn("'Spell Affinity'", generator)
        self.assertNotIn("shutil.rmtree", generator)

        if AGGREGATE.is_file():
            aggregate = AGGREGATE.read_text(encoding="utf-8-sig")
            self.assertGreaterEqual(aggregate.count(BOOK_AFFINITY), 3)
            self.assertGreaterEqual(aggregate.count(SPELL_AFFINITY), 11)
            self.assertNotIn(
                "Coût Alternatif — Si vous contrôlez 1 créature “Spellbook”",
                aggregate,
            )

    def test_all_images_resolve(self) -> None:
        for filename in EXPECTED_RULES:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image = next(
                line.split(": ", 1)[1]
                for line in text.splitlines()
                if line.startswith("\timage: ")
            )
            self.assertTrue((PROJECT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
