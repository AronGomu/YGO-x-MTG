from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT = REPO_ROOT / "MSE_projects" / "09_YGO_Non_Archetype_Non_Creatures.mse-set"

EXPECTED_CARDS = (
    "card allure of darkness",
    "card book of eclipse",
    "card book of moon",
    "card breakthrough skill",
    "card compulsory evacuation device",
    "card dark hole",
    "card foolish burial",
    "card instant fusion",
    "card karma cut",
    "card monster reborn",
    "card mystical space typhoon",
    "card phoenix wing wind blast",
    "card raigeki",
    "card super polymerization",
    "card torrential tribute",
    "card twin twisters",
    "card upstart goblin",
)

EXPECTED_FRAGMENTS = {
    "card allure of darkness": ("Piochez 2 cartes", "exilez 1 carte noire"),
    "card book of eclipse": ("Retournez toutes les créatures face verso",),
    "card book of moon": ("Retournez la créature ciblée face verso",),
    "card breakthrough skill": (
        "La créature ciblée perd toutes ses capacités",
        "depuis votre Grave",
    ),
    "card compulsory evacuation device": (
        "Renvoyez le permanent non-terrain ciblé dans la main",
    ),
    "card dark hole": ("Détruisez toutes les créatures",),
    "card foolish burial": ("depuis votre Deck au Grave",),
    "card instant fusion": (
        "<b>Summon</b>",
        "en ignorant les restrictions de Summon",
    ),
    "card karma cut": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte",
        "Exilez la créature ciblée",
    ),
    "card monster reborn": ("depuis 1 Grave",),
    "card mystical space typhoon": (
        "Détruisez le permanent non-créature non-terrain ciblé",
    ),
    "card phoenix wing wind blast": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte",
        "au-dessus du Deck",
    ),
    "card raigeki": ("Détruisez toutes les créatures que vos adversaires contrôlent",),
    "card super polymerization": ("<b>Fusion Summon</b>",),
    "card torrential tribute": (
        "Vous ne pouvez lancer ce sort que si 1 créature est arrivée",
        "Détruisez toutes les créatures",
    ),
    "card twin twisters": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte",
        "Détruisez jusqu",
    ),
    "card upstart goblin": ("Piochez 1 carte", "Coût Alternatif"),
}


def rule_block(text: str) -> str:
    match = re.search(
        r"(?ms)^\trule_text:(?:\n(?P<body>(?:\t\t.*\n)+?)|(?P<inline>.*)\n)(?=^\tflavor_text:)",
        text,
    )
    if not match:
        return ""
    if match.group("body") is not None:
        return match.group("body")
    return match.group("inline") or ""


class NonArchetypeNonCreatureTests(unittest.TestCase):
    def test_set_references_every_card_once(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = [
            line.removeprefix("include_file: ")
            for line in set_text.splitlines()
            if line.startswith("include_file: ")
        ]
        self.assertEqual(includes, sorted(EXPECTED_CARDS))
        self.assertEqual(len(includes), len(set(includes)))

    def test_every_mse_card_uses_the_updated_rule_contract(self) -> None:
        stale_terms = (
            "bibliothèque",
            "cimetière",
            "GYD",
            "champ de bataille",
            "défaussez-vous",
        )
        for filename in EXPECTED_CARDS:
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                self.assertEqual(text.count("(1 - Résolution)"), 1)
                for fragment in EXPECTED_FRAGMENTS[filename]:
                    self.assertIn(fragment, text)
                body = rule_block(text)
                self.assertTrue(body)
                for stale_term in stale_terms:
                    self.assertNotIn(stale_term, body)
                self.assertNotIn("error-spelling", body)
                self.assertRegex(text, r"(?m)^\tsub_type:\s*$")

    def test_fusion_actions_use_current_types_and_keywords(self) -> None:
        instant_fusion = (PROJECT / "card instant fusion").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn(
            "super_type: <word-list-type-en>Sorcery</word-list-type-en>",
            instant_fusion,
        )
        self.assertIn("<b>Summon</b>", instant_fusion)
        self.assertIn("en ignorant les restrictions de Summon", instant_fusion)

        super_polymerization = (PROJECT / "card super polymerization").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn(
            "super_type: <word-list-type-en>Fusion Summon Instant</word-list-type-en>",
            super_polymerization,
        )
        self.assertIn("<b>Fusion Summon</b>", super_polymerization)

    def test_all_image_references_resolve(self) -> None:
        for filename in EXPECTED_CARDS:
            text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            image = next(
                line.split(": ", 1)[1]
                for line in text.splitlines()
                if line.startswith("\timage: ")
            )
            self.assertTrue((PROJECT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
