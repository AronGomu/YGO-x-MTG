from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAP_CARDS = (
    (
        "Breakthrough Skill",
        ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card breakthrough skill",
    ),
    (
        "Compulsory Evacuation Device",
        ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card compulsory evacuation device",
    ),
    (
        "Karma Cut",
        ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card karma cut",
    ),
    (
        "Phoenix Wing Wind Blast",
        ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card phoenix wing wind blast",
    ),
    (
        "Torrential Tribute",
        ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set/card torrential tribute",
    ),
    (
        "Burning Abyss - Fire Lake",
        ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card burning abyss - fire lake",
    ),
    (
        "Burning Abyss - Traveler",
        ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card burning abyss - traveler",
    ),
    (
        "Fiend Griefing",
        ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card fiend griefing",
    ),
)


class TrapSupertypeTests(unittest.TestCase):
    def test_trap_cards_use_supertype_without_old_keyword(self) -> None:
        for card_name, card_path in TRAP_CARDS:
            with self.subTest(card=card_name):
                card = card_path.read_text(encoding="utf-8-sig")
                self.assertIn(
                    "super_type: <word-list-type-en>Trap Instant</word-list-type-en>",
                    card,
                )
                self.assertRegex(card, r"(?m)^\tsub_type:\s*$")
                self.assertNotIn("<b>Piège</b>", card)

    def test_trap_references_use_current_vocabulary(self) -> None:
        rafflesia_path = (
            ROOT / "MSE_projects/07_YGO_Staples_Xyz.mse-set/card traptrix rafflesia"
        )
        rafflesia = rafflesia_path.read_text(encoding="utf-8-sig")
        self.assertIn("<i>2 créatures MV 1</i>", rafflesia)
        self.assertIn("1 Trap depuis votre Deck au Grave", rafflesia)
        self.assertNotIn("error-spelling", rafflesia)

        back_jack_path = (
            ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set/card absolute king back jack"
        )
        back_jack = back_jack_path.read_text(encoding="utf-8-sig")
        self.assertIn("Si c’est une Trap, <b>Set</b> la carte", back_jack)
        self.assertIn("vous pouvez la lancer ce tour-ci", back_jack)

    def test_rule_and_generator_sources_use_trap_as_supertype(self) -> None:
        context = (ROOT / "docs/context.md").read_text(encoding="utf-8-sig")
        detailed = (ROOT / "docs/02_rules_keywords_card_design.md").read_text(
            encoding="utf-8-sig"
        )
        for rules in (context, detailed):
            self.assertIn("Super-type Trap", rules)
            self.assertIn("`Trap Instant`", rules)
            self.assertIn("lancée depuis le terrain", rules)

        generator = (ROOT / ".script/create_archetype_projects.py").read_text(
            encoding="utf-8-sig"
        )
        keyword_line = next(line for line in generator.splitlines() if line.startswith("KEYWORDS"))
        self.assertNotIn("'Piège'", keyword_line)
        self.assertIn("source_super_type", generator)

        aggregate = (ROOT / "mse/set").read_text(encoding="utf-8-sig")
        self.assertGreaterEqual(aggregate.count("\tsuper type: Trap"), 5)
        self.assertNotIn("\tsub type: Piège", aggregate)


if __name__ == "__main__":
    unittest.main()
