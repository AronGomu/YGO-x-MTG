from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "10_YGO_Burning_Abyss.mse-set"
DOCUMENT = ROOT / "docs" / "10_archetype_burning_abyss.md"


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

    def test_images_and_collection_numbers_resolve(self) -> None:
        for index, include in enumerate(self.includes, 1):
            with self.subTest(card=include):
                text = (PROJECT / include).read_text(encoding="utf-8-sig")
                image = re.search(r"(?m)^\timage:\s*(.*)$", text)
                self.assertIsNotNone(image)
                if image and image.group(1).strip():
                    self.assertTrue((PROJECT / image.group(1).strip()).is_file())
                codes = re.findall(r"(?m)^\tcard_code_text(?:_\d+)?:\s*(.*)$", text)
                self.assertTrue(codes)
                for code in codes:
                    self.assertTrue(code.startswith(f"{index:03d}/030 "))

    def test_render_names_match_card_names_exactly(self) -> None:
        expected_names = set()
        for include in self.includes:
            text = (PROJECT / include).read_text(encoding="utf-8-sig")
            name = re.search(r"(?m)^\tname:\s*(.+)$", text)
            self.assertIsNotNone(name)
            assert name is not None
            expected_names.add(f"{name.group(1).strip()}.png")
        self.assertEqual({path.name for path in (PROJECT / "render").glob("*.png")}, expected_names)

    def test_accepted_vocabulary_and_card_changes_are_preserved(self) -> None:
        expected = {
            "card aa-zeus - sky thunder": (
                "<i>2 créatures MV 4</i>",
                "Déclenchable Soft",
                "<b>On Creature you Control Destroy</b>",
                "<b>Attach</b>",
            ),
            "card burning abyss - cherubini": (
                "<i>2 Creatures MV 1</i>",
                "<b>Bounded 1</b>",
                "toughness: 1",
            ),
            "card burning abyss - dante pilgrim": ("<b>Défense talismanique</b>",),
            "card burning abyss - farfa": ("<b>Slow Blink 1 Any Creature</b>",),
            "card burning abyss - good  evil": (
                "super_type: <word-list-type-en>Ritual Summon Sorcery</word-list-type-en>",
                "<b>Ritual Summon</b>",
            ),
            "card burning abyss - terminus": (
                "super_type: <word-list-type-en>Fusion Summon Sorcery</word-list-type-en>",
                "<b>Fusion Summon</b>",
            ),
            "card leviair the sea dragon": (
                "<word-list-race-en>Dragon</word-list-race-en>",
                "créature MV 1 exilée",
            ),
            "card burning abyss - fire lake": (
                "super_type: <word-list-type-en>Trap Instant</word-list-type-en>",
            ),
            "card burning abyss - traveler": (
                "super_type: <word-list-type-en>Trap Instant</word-list-type-en>",
            ),
            "card fiend griefing": (
                "super_type: <word-list-type-en>Trap Instant</word-list-type-en>",
            ),
        }
        for filename, fragments in expected.items():
            with self.subTest(card=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                for fragment in fragments:
                    self.assertIn(fragment, text)

    def test_burning_abyss_uses_Grave_consistently(self) -> None:
        for include in self.includes:
            text = (PROJECT / include).read_text(encoding="utf-8-sig")
            self.assertNotRegex(text, r"\bGY\b")
        document = DOCUMENT.read_text(encoding="utf-8-sig")
        self.assertNotRegex(document, r"\bGY\b")
        self.assertIn("**On Send Grave**", document)

    def test_accepted_rules_are_documented(self) -> None:
        context = (ROOT / "docs" / "context.md").read_text(encoding="utf-8-sig")
        detailed = (ROOT / "docs" / "02_rules_keywords_card_design.md").read_text(
            encoding="utf-8-sig"
        )
        for fragment in (
            "**Summon** signifie",
            "**Reanimate** signifie",
            "**Bounded X**",
            "**Indestructible contre les effets**",
            "**Défense talismanique**",
            "**Slow Blink X Any Creature**",
            "**Ritual Summon**",
            "**Fusion Summon**",
            "**On Send Grave**",
        ):
            self.assertIn(fragment, context)
        self.assertIn("### On Creature you Control Destroy", detailed)
        self.assertIn("## Super-type Trap", detailed)
        self.assertIn("`Trap Instant`", detailed)
        self.assertIn("contourne explicitement et uniquement l’attente d’un tour", detailed)
        self.assertIn("en ignorant les restrictions de Summon", detailed)
        self.assertIn("toujours demander à l’utilisateur", detailed)
        self.assertIn("ne constitue pas une invocation correcte", detailed)
        self.assertIn("uniquement tant que son bounder reste sur le terrain", detailed)

    def test_illegal_summon_workflows_require_user_confirmation(self) -> None:
        skill_paths = (
            ".agents/skills/add-ygo-card/SKILL.md",
            ".agents/skills/update-card-from-ai/SKILL.md",
            ".agents/skills/validate-mse-updates/SKILL.md",
            ".agents/skills/normalize-card-formatting/SKILL.md",
        )
        for relative_path in skill_paths:
            with self.subTest(skill=relative_path):
                skill = (ROOT / relative_path).read_text(encoding="utf-8-sig")
                self.assertIn("AskUserQuestion", skill)
                self.assertIn("en ignorant les restrictions de Summon", skill)
                self.assertIn("Never infer or insert the bypass silently", skill)
                self.assertIn("does not make it a correct invocation", skill)

    def test_mse_to_markdown_sync_is_the_only_burning_abyss_updater(self) -> None:
        self.assertTrue((ROOT / ".script" / "sync_burning_abyss_from_mse.py").is_file())
        self.assertFalse((ROOT / ".script" / "update_burning_abyss_from_md.py").exists())
        self.assertFalse((ROOT / ".script" / "update_burning_abyss_mse.py").exists())
        archetype_generator = (ROOT / ".script" / "create_archetype_projects.py").read_text(
            encoding="utf-8-sig"
        )
        self.assertNotIn("10_archetype_burning_abyss.md", archetype_generator)


if __name__ == "__main__":
    unittest.main()
