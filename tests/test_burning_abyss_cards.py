from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects/10_YGO_Burning_Abyss.mse-set"
DOCUMENT = ROOT / "docs/10_archetype_burning_abyss.md"


class BurningAbyssCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        cls.includes = re.findall(r"(?m)^include_file:\s*(.+)$", cls.set_text)

    def test_manifest_has_complete_unique_card_graph(self) -> None:
        self.assertEqual(len(self.includes), 30)
        self.assertEqual(len(set(self.includes)), 30)
        self.assertEqual({path.name for path in PROJECT.glob("card *")}, set(self.includes))
        self.assertIn("title: YGO x MTG -- Burning Abyss", self.set_text)
        self.assertIn("set_language: EN", self.set_text)
        self.assertIn("card_language: English", self.set_text)

    def test_images_and_collection_numbers_resolve(self) -> None:
        for index, include in enumerate(self.includes, 1):
            with self.subTest(card=include):
                text = (PROJECT / include).read_text(encoding="utf-8-sig")
                image_match = re.search(r"(?m)^\timage:\s*(.*)$", text)
                self.assertIsNotNone(image_match)
                if image_match and image_match.group(1).strip():
                    self.assertTrue((PROJECT / image_match.group(1).strip()).is_file())
                codes = re.findall(r"(?m)^\tcard_code_text(?:_\d+)?:\s*(.+)$", text)
                self.assertTrue(codes)
                for code in codes:
                    self.assertRegex(code, rf"^{index:03d}/030 [CURM]$")

    def test_representative_card_mechanics_are_preserved(self) -> None:
        expected = {
            "card aa-zeus - sky thunder": (
                "<i>2 creatures MV 4</i>",
                "Xyz Alternative Cost",
                "(1 - Activated <kw-a><nospellcheck><key>Flash</key></nospellcheck></kw-a> Soft)",
                "<b>Detach 2</b>",
                "send all other nonland permanents on the field to <b>Grave</b>",
                "(2 - Triggered Soft)",
                "<b>Attach</b> the destroyed creature to ZEUS",
            ),
            "card burning abyss - cherubini": (
                "name: Burning Abyss - Cherubini",
                "super_type: <word-list-type-en>Link Lvl 2 Creature</word-list-type-en>",
                "<i>2 creatures MV 1</i>",
                "Send 1 creature with MV 1 from your Deck to <b>Grave</b>",
            ),
            "card burning abyss - dante pilgrim": (
                "<b><kw-a><nospellcheck><key>Hexproof</key></nospellcheck></kw-a></b>",
                "<b>On Destroy</b>",
                "they discard 1 card at random",
            ),
            "card burning abyss - farfa": (
                "<b>Slow Blink 1 Any Creature</b>",
            ),
            "card burning abyss - good  evil": (
                "<b>Ritual Summon</b>",
                "<b>Exile from Grave</b> and discard 1 “Burning Abyss” creature",
            ),
            "card burning abyss - terminus": (
                "<b>Fusion Summon</b>",
                "the target gains +2/+2 until the end of the opponent’s next turn",
            ),
            "card leviair the sea dragon": (
                "target 1 exiled MV 1 creature",
                "<b>Release</b> the target",
            ),
        }
        for card, fragments in expected.items():
            text = (PROJECT / card).read_text(encoding="utf-8-sig")
            for fragment in fragments:
                with self.subTest(card=card, fragment=fragment):
                    self.assertIn(fragment, text)

    def test_trap_and_extra_deck_types_use_current_contract(self) -> None:
        trap = (PROJECT / "card burning abyss - fire lake").read_text(encoding="utf-8-sig")
        self.assertIn("super_type: <word-list-type-en>Trap Instant</word-list-type-en>", trap)
        self.assertIn("sub_type:", trap)
        self.assertNotIn("sub_type: <word-list-race-en>Trap", trap)
        for name in (
            "card aa-zeus - sky thunder",
            "card beatrice lady of the eternal",
            "card burning abyss - dante",
            "card downerd magician",
            "card leviair the sea dragon",
        ):
            text = (PROJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("super_type: <word-list-type-en>Xyz Creature</word-list-type-en>", text)

    def test_accepted_general_rules_are_documented_in_english(self) -> None:
        context = (ROOT / "docs/context.md").read_text(encoding="utf-8-sig")
        general = (ROOT / "docs/02_rules_keywords_card_design.md").read_text(encoding="utf-8-sig")
        archetype = DOCUMENT.read_text(encoding="utf-8-sig")
        self.assertIn("**Summon** means", context)
        self.assertIn("**Reclaim** means", context)
        self.assertIn("**On Opponent Creature Enter** means", context)
        self.assertIn("### Summon", general)
        self.assertIn("### Reclaim", general)
        self.assertIn("### On Opponent Creature Enter", general)
        self.assertIn("## Card source of truth", archetype)
        self.assertIn("Card-by-card values for this archetype exist only", archetype)

    def test_skills_reject_illegal_summon_bypass(self) -> None:
        for relative in (
            ".agents/skills/add-ygo-card/SKILL.md",
            ".agents/skills/update-card-from-ai/SKILL.md",
            ".agents/skills/fix-mse-cards/SKILL.md",
            ".agents/skills/normalize-card-formatting/SKILL.md",
        ):
            with self.subTest(skill=relative):
                text = (ROOT / relative).read_text(encoding="utf-8-sig")
                self.assertIn("Summon", text)
                self.assertRegex(text, r"(?i)illegal|incorrect|not.*proper|does not.*proper")
                self.assertRegex(text, r"(?i)user|review|decision|confirmation")

    def test_retired_sync_cannot_overwrite_canonical_project(self) -> None:
        script = (ROOT / ".script/sync_burning_abyss_from_mse.py").read_text(encoding="utf-8-sig")
        self.assertIn("Retired", script)
        self.assertIn("canonical MSE project", script)
        self.assertNotIn("shutil.copy2", script)

    def test_render_directory_has_expected_outputs(self) -> None:
        render_dir = PROJECT / "render"
        renders = list(render_dir.glob("*.png"))
        self.assertEqual(len(renders), len(self.includes))


if __name__ == "__main__":
    unittest.main()
