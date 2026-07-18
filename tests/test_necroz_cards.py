from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "12_YGO_Necroz.mse-set"
DOC = ROOT / "docs" / "12_archetype_necroz.md"

INCLUDED = [
    "card herald of the arc light",
    "card manju of the ten thousand hands",
    "card nekroz - brionac",
    "card nekroz - catastor",
    "card nekroz - clausolas",
    "card nekroz - cycle",
    "card nekroz - dance princess",
    "card nekroz - decisive armor",
    "card nekroz - exa",
    "card nekroz - great sorcerer",
    "card nekroz - gungnir",
    "card nekroz - kaleidoscope",
    "card nekroz - mirror",
    "card nekroz - shurit",
    "card nekroz - trishula",
    "card nekroz - unicore",
    "card nekroz - valkyrus",
    "card preparation of rites",
    "card senju of the thousand hands",
]


class NecrozCardTests(unittest.TestCase):
    def test_manifest_includes_all_active_cards(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = re.findall(r"(?m)^include_file:\s*(.+)$", set_text)
        self.assertEqual(includes, INCLUDED)
        self.assertEqual(len(includes), 19)

    def test_included_cards_clean_and_images_resolve(self) -> None:
        stale = ("cimetière", "GYD", "bibliothèque", "valeur de mana", "error-spelling")
        for filename in INCLUDED:
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                rule = text.split("\trule_text:\n", 1)[1].split("\tflavor_text:", 1)[0]
                for term in stale:
                    self.assertNotIn(term, rule)
                self.assertNotIn("\tGY", rule)
                image = next(
                    line.split(": ", 1)[1]
                    for line in text.splitlines()
                    if line.startswith("\timage: ")
                )
                self.assertTrue((PROJECT / image).is_file(), image)

    def test_key_mechanics_present(self) -> None:
        brionac = (PROJECT / "card nekroz - brionac").read_text(encoding="utf-8-sig")
        self.assertIn("<b>Bounce</b>", brionac)
        self.assertIn("Défaussez Brionac", brionac)

        catastor = (PROJECT / "card nekroz - catastor").read_text(encoding="utf-8-sig")
        self.assertIn("<b>Reanimate</b>", catastor)

        exa = (PROJECT / "card nekroz - exa").read_text(encoding="utf-8-sig")
        self.assertIn("<b>Release</b>", exa)
        self.assertIn("en ignorant les restrictions de Summon", exa)

        unicore = (PROJECT / "card nekroz - unicore").read_text(encoding="utf-8-sig")
        self.assertIn("<b>Salvage</b>", unicore)

        sorcerer = (PROJECT / "card nekroz - great sorcerer").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("<b>Reclaim</b>", sorcerer)

        for name in (
            "card nekroz - cycle",
            "card nekroz - kaleidoscope",
            "card nekroz - mirror",
        ):
            text = (PROJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("<b>Ritual Summon</b>", text)
            self.assertIn("<b>Nekroz Recovery</b>", text)
            self.assertIn("cherchez 1 non-créature Ritual Summon “Nekroz”", text)

    def test_archetype_doc_points_at_mse(self) -> None:
        doc = DOC.read_text(encoding="utf-8-sig")
        self.assertIn("MSE_projects/12_YGO_Necroz.mse-set", doc)
        self.assertIn("**Nekroz Recovery**", doc)
        self.assertIn("1 non-créature Ritual Summon “Nekroz”", doc)


if __name__ == "__main__":
    unittest.main()
