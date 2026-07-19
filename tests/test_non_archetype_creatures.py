from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "03_YGO_Non_Archetype_Creatures.mse-set"

EXPECTED_CARDS = {
    "card ash blossom  joyous spring": (
        "name: Ash Blossom & Joyous Spring",
        "casting_cost: R",
        "super_type: <word-list-type-en>Tuner Creature</word-list-type-en>",
        "sub_type: <word-list-race-en>Zombie</word-list-race-en>",
        "(1 - Activated",
        "Flash",
        "Hard)",
        "counter it",
        "power: 0",
        "toughness: 1",
        "card_code_text: 001/004 C",
    ),
    "card d.d crow": (
        "name: D.D. Crow",
        "casting_cost: B",
        "sub_type: <word-list-race-en>Bird</word-list-race-en>",
        "(1 - Activated",
        "target 1 card in 1 Grave; exile it",
        "card_code_text: 002/004 C",
    ),
    "card effect veiler": (
        "name: Effect Veiler",
        "casting_cost: W",
        "sub_type: <word-list-race-en>Wizard</word-list-race-en>",
        "the target loses all its abilities",
        "card_code_text: 003/004 C",
    ),
    "card maxx  c": (
        "name: Maxx “C”",
        "casting_cost: G",
        "sub_type: <word-list-race-en>Insect</word-list-race-en>",
        "draw 1 card <b>On Opponent Creature Enter</b>",
        "card_code_text: 004/004 C",
    ),
}


class NonArchetypeCreatureTests(unittest.TestCase):
    def test_mse_cards_match_english_contract(self) -> None:
        for filename, fragments in EXPECTED_CARDS.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                for fragment in fragments:
                    self.assertIn(fragment, text)
                self.assertNotIn("error-spelling", text)

    def test_set_references_exactly_the_cards(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = {
            line.removeprefix("include_file: ")
            for line in set_text.splitlines()
            if line.startswith("include_file: ")
        }
        self.assertEqual(includes, set(EXPECTED_CARDS))
        self.assertIn("set_language: EN", set_text)
        self.assertIn("card_language: English", set_text)

    def test_on_opponent_creature_enter_is_documented(self) -> None:
        rules = (ROOT / "docs/02_rules_keywords_card_design.md").read_text(encoding="utf-8-sig")
        context = (ROOT / "docs/context.md").read_text(encoding="utf-8-sig")
        self.assertIn("### On Opponent Creature Enter", rules)
        self.assertIn("**On Opponent Creature Enter** means", context)

    def test_legacy_aggregate_cannot_restore_card_data(self) -> None:
        self.assertFalse((ROOT / "mse/set").exists())
        self.assertTrue((ROOT / "mse/French/set").is_file())
        generator = (ROOT / ".script/create_archetype_projects.py").read_text(encoding="utf-8-sig")
        self.assertIn("Retired", generator)
        self.assertIn("English folder-form projects", generator)

    def test_all_image_references_resolve(self) -> None:
        for filename in EXPECTED_CARDS:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image = next(line.split(": ", 1)[1] for line in text.splitlines() if line.startswith("\timage: "))
            self.assertTrue((PROJECT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
