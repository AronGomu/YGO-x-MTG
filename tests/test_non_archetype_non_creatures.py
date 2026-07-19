from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set"

EXPECTED = {
    "card allure of darkness": ("Draw 2 cards", "exile 1 black card"),
    "card book of eclipse": ("Turn all creatures face down",),
    "card book of moon": ("Turn target creature face down",),
    "card breakthrough skill": ("Target creature loses all its abilities", "from your Grave"),
    "card compulsory evacuation device": ("Return target nonland permanent",),
    "card dark hole": ("Destroy all creatures",),
    "card foolish burial": ("from your Deck to <b>Grave</b>",),
    "card instant fusion": ("<b>Summon</b>", "ignoring the restrictions of Summon"),
    "card karma cut": ("As an additional cost to cast this spell, discard 1 card", "Exile target creature"),
    "card monster reborn": ("in 1 <b>Grave</b>", "<b>Reanimate</b> the target"),
    "card mystical space typhoon": ("Target 1 nonland noncreature permanent; destroy the target",),
    "card phoenix wing wind blast": ("discard 1 card", "on top of its owner's Deck"),
    "card raigeki": ("Destroy all creatures your opponents control",),
    "card super polymerization": ("<b>Fusion Summon</b>",),
    "card torrential tribute": ("cast this spell only if 1 creature has entered", "Destroy all creatures"),
    "card twin twisters": ("discard 1 card", "Target up to 2 nonland noncreature permanents; destroy the targets"),
    "card upstart goblin": ("Draw 1 card", "Alternative Cost"),
}


def rule_block(text: str) -> str:
    match = re.search(r"(?ms)^\trule_text:(?:\n(?P<body>(?:\t\t.*\n)+?)|(?P<inline>.*)\n)(?=^\tflavor_text:)", text)
    if not match:
        return ""
    return match.group("body") if match.group("body") is not None else (match.group("inline") or "")


class NonArchetypeNonCreatureTests(unittest.TestCase):
    def test_manifest_references_every_card_once(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = [line.removeprefix("include_file: ") for line in set_text.splitlines() if line.startswith("include_file: ")]
        self.assertEqual(includes, sorted(EXPECTED))
        self.assertEqual(len(includes), len(set(includes)))

    def test_every_card_uses_english_rule_contract(self) -> None:
        stale = ("library", "graveyard", "GYD", "battlefield", "Résolution", "Déclenchable")
        for filename, fragments in EXPECTED.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                self.assertEqual(text.count("(1 - Resolution)"), 1)
                for fragment in fragments:
                    self.assertIn(fragment, text)
                body = rule_block(text)
                self.assertTrue(body)
                for term in stale:
                    self.assertNotIn(term, body)
                self.assertNotIn("error-spelling", body)
                self.assertRegex(text, r"(?m)^\tsub_type:\s*$")

    def test_fusion_actions_use_current_types_and_keywords(self) -> None:
        instant = (PROJECT / "card instant fusion").read_text(encoding="utf-8-sig")
        self.assertIn("super_type: <word-list-type-en>Sorcery</word-list-type-en>", instant)
        self.assertIn("<b>Summon</b>", instant)
        self.assertIn("ignoring the restrictions of Summon", instant)

        super_poly = (PROJECT / "card super polymerization").read_text(encoding="utf-8-sig")
        self.assertIn("super_type: <word-list-type-en>Fusion Summon Instant</word-list-type-en>", super_poly)
        self.assertIn("<b>Fusion Summon</b>", super_poly)

    def test_all_image_references_resolve(self) -> None:
        for filename in EXPECTED:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image = next(line.split(": ", 1)[1] for line in text.splitlines() if line.startswith("\timage: "))
            self.assertTrue((PROJECT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
