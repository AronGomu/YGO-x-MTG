from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT = REPO_ROOT / "MSE_projects" / "03_YGO_Non_Archetype_Creatures.mse-set"

# Filenames match the active MSE set includes (MSE-safe slug forms).
EXPECTED_CARDS = {
    "card ash blossom  joyous spring": (
        "name: Ash Blossom & Joyous Spring",
        "casting_cost: R",
        "super_type: <word-list-type-en>Tuner Creature</word-list-type-en>",
        "sub_type: <word-list-race-en>Zombie</word-list-race-en>",
        "(1 - Activable",
        "Flash",
        "Hard)",
        "power: 0",
        "toughness: 1",
        "card_code_text: 001/004 C",
        "contrecarrez-le",
    ),
    "card d.d crow": (
        "name: D.D Crow",
        "casting_cost: B",
        "sub_type: <word-list-race-en>Bird</word-list-race-en>",
        "(1 - Activable",
        "Flash",
        "power: 0",
        "toughness: 1",
        "card_code_text: 002/004 C",
        "dans 1 Grave",
    ),
    "card effect veiler": (
        "name: Effect Veiler",
        "casting_cost: W",
        "super_type: <word-list-type-en>Tuner Creature</word-list-type-en>",
        "sub_type: <word-list-race-en>Wizard</word-list-race-en>",
        "(1 - Activable",
        "Flash",
        "power: 0",
        "toughness: 1",
        "card_code_text: 003/004 C",
        "perd toutes ses capacités",
    ),
    "card maxx  c": (
        "name: Maxx « C »",
        "casting_cost: G",
        "sub_type: <word-list-race-en>Insect</word-list-race-en>",
        "(1 - Activable",
        "Flash",
        "Hard)",
        "<b>On Opponent Creature Enter</b>",
        "power: 0",
        "toughness: 1",
        "card_code_text: 004/004 C",
    ),
}


class NonArchetypeCreatureTests(unittest.TestCase):
    def test_mse_cards_match_updated_contract(self) -> None:
        for filename, expected_fragments in EXPECTED_CARDS.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                for fragment in expected_fragments:
                    self.assertIn(fragment, text)
                self.assertNotIn("error-spelling", text)

    def test_set_references_exactly_the_updated_cards(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = {
            line.removeprefix("include_file: ")
            for line in set_text.splitlines()
            if line.startswith("include_file: ")
        }
        self.assertEqual(includes, set(EXPECTED_CARDS))
        self.assertFalse((PROJECT / "card corbeau d d").exists())

    def test_rules_document_on_opponent_creature_enter(self) -> None:
        rules = (REPO_ROOT / "docs" / "02_rules_keywords_card_design.md").read_text(
            encoding="utf-8-sig"
        )
        context = (REPO_ROOT / "docs" / "context.md").read_text(encoding="utf-8-sig")
        self.assertIn("### On Opponent Creature Enter", rules)
        self.assertIn("**On Opponent Creature Enter** signifie", context)

    def test_generators_do_not_restore_old_card_data(self) -> None:
        for relative_path in (
            ".script/download_ygo_images.py",
            ".script/generate_original_cards.py",
            "MSE_projects/ensure_original_images.py",
        ):
            text = (REPO_ROOT / relative_path).read_text(encoding="utf-8-sig")
            self.assertNotIn("Corbeau D.D.", text)

        downloader = (REPO_ROOT / ".script" / "download_ygo_images.py").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn('ROOT.glob("*_YGO_*.mse-set")', downloader)

        aggregate = (REPO_ROOT / "mse" / "set").read_text(encoding="utf-8-sig")
        self.assertIn("name: D.D Crow", aggregate)
        self.assertIn("On Opponent Creature Enter", aggregate)
        self.assertNotIn("name: Corbeau D.D.", aggregate)
        for name in (
            "Ash Blossom & Joyous Spring",
            "D.D Crow",
            "Effect Veiler",
            "Maxx « C »",
        ):
            self.assertIn(f"\tname: {name}\n", aggregate)

    def test_all_image_references_resolve(self) -> None:
        for filename in EXPECTED_CARDS:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image_line = next(
                line for line in text.splitlines() if line.startswith("\timage: ")
            )
            self.assertTrue((PROJECT / image_line.split(": ", 1)[1]).is_file())


if __name__ == "__main__":
    unittest.main()
