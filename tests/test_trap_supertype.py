from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAP_CARDS = (
    ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card breakthrough skill",
    ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card compulsory evacuation device",
    ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card karma cut",
    ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card phoenix wing wind blast",
    ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card torrential tribute",
    ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card burning abyss - fire lake",
    ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card burning abyss - traveler",
    ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card fiend griefing",
)


class TrapSupertypeTests(unittest.TestCase):
    def test_trap_cards_use_supertype_without_old_keyword(self) -> None:
        for card_path in TRAP_CARDS:
            with self.subTest(card=card_path.name):
                card = card_path.read_text(encoding="utf-8-sig")
                self.assertIn("super_type: <word-list-type-en>Trap Instant</word-list-type-en>", card)
                self.assertRegex(card, r"(?m)^\tsub_type:(?: <word-list-spell></word-list-spell>)?\s*$")
                self.assertNotIn("<b>Trap</b>", card)

    def test_trap_references_use_current_english_vocabulary(self) -> None:
        rafflesia = (ROOT / "MSE_projects/07_YGO_Staples_Xyz.mse-set/card traptrix rafflesia").read_text(encoding="utf-8-sig")
        self.assertIn("<i>2 Creatures MV 1</i>", rafflesia)
        self.assertIn("<b>Send</b> 1 Trap from your Deck to Grave", rafflesia)
        self.assertNotIn("error-spelling", rafflesia)

        back_jack = (ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card absolute king back jack").read_text(encoding="utf-8-sig")
        self.assertIn("If it is a Trap, <b>Set</b> the card face down on the Field", back_jack)
        self.assertIn("you may <b>Cast</b> it this turn", back_jack)

    def test_rules_and_archive_preserve_trap_contract(self) -> None:
        context = (ROOT / "docs/context.md").read_text(encoding="utf-8-sig")
        detailed = (ROOT / "docs/02_rules_keywords_card_design.md").read_text(encoding="utf-8-sig")
        for rules in (context, detailed):
            self.assertIn("Super-type Trap", rules)
            self.assertIn("`Trap Instant`", rules)
            self.assertIn("cast it from", rules)

        generator = (ROOT / ".script/create_archetype_projects.py").read_text(encoding="utf-8-sig")
        self.assertIn("Retired", generator)
        self.assertNotIn("shutil.copy2", generator)

        self.assertFalse((ROOT / "mse/set").exists())
        aggregate = (ROOT / "mse/French/set").read_text(encoding="utf-8-sig")
        self.assertGreaterEqual(aggregate.count("\tsuper type: Trap"), 5)
        self.assertNotIn("\tsub type: Trap", aggregate)


if __name__ == "__main__":
    unittest.main()
