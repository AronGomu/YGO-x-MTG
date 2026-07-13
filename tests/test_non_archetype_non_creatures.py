from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT = REPO_ROOT / "MSE_projects" / "09_YGO_Non_Archetype_Non_Creatures.mse-set"
DOC = REPO_ROOT / "docs" / "09_non_archetype_non_creature.md"

EXPECTED_RULES = {
    "card allure of darkness": (
        "(1 - Résolution) Piochez 2 cartes, puis exilez 1 carte noire de votre main. Si vous ne le faites pas, défaussez votre main.",
    ),
    "card book of eclipse": (
        "(1 - Résolution) Retournez toutes les créatures face verso.",
    ),
    "card book of moon": (
        "(1 - Résolution) Retournez la créature ciblée face verso.",
    ),
    "card breakthrough skill": (
        "(1 - Résolution) La créature ciblée perd toutes ses capacités jusqu’à la fin du tour.",
        "(2 - Passif) Vous pouvez lancer cette carte depuis votre GYD.",
    ),
    "card compulsory evacuation device": (
        "(1 - Résolution) Renvoyez le permanent non-terrain ciblé dans la main de son propriétaire.",
    ),
    "card dark hole": ("(1 - Résolution) Détruisez toutes les créatures.",),
    "card foolish burial": (
        "(1 - Résolution) Envoyez 1 carte de créature depuis votre Deck au GYD.",
    ),
    "card instant fusion": (
        "(1 - Résolution) <b>Summon</b> 1 Fusion Creature MV 1 depuis votre Sideboard en ignorant les restrictions de Summon.",
    ),
    "card karma cut": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte.",
        "(1 - Résolution) Exilez la créature ciblée.",
    ),
    "card monster reborn": (
        "(1 - Résolution) Renvoyez sur le terrain sous votre contrôle 1 carte de créature ciblée depuis 1 GYD.",
    ),
    "card mystical space typhoon": (
        "(1 - Résolution) Détruisez le permanent non-créature non-terrain ciblé.",
    ),
    "card phoenix wing wind blast": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte.",
        "(1 - Résolution) Mettez le permanent ciblé au-dessus du Deck de son propriétaire.",
    ),
    "card raigeki": (
        "(1 - Résolution) Détruisez toutes les créatures que vos adversaires contrôlent.",
    ),
    "card super polymerization": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte.",
        "(1 - Résolution) Exilez 1 ou plusieurs créatures du terrain comme matériaux ; <b>Fusion Summon</b>",
    ),
    "card torrential tribute": (
        "Vous ne pouvez lancer ce sort que si 1 créature est arrivée sur le terrain ce tour-ci.",
        "(1 - Résolution) Détruisez toutes les créatures.",
    ),
    "card twin twisters": (
        "En tant que coût supplémentaire pour lancer ce sort, défaussez 1 carte.",
        "(1 - Résolution) Détruisez jusqu’à 2 permanents non-créature non-terrain ciblés.",
    ),
    "card upstart goblin": (
        "Coût Alternatif — Vous pouvez lancer ce sort sans payer son coût de mana.",
        "(1 - Résolution) Piochez 1 carte.",
    ),
}


class NonArchetypeNonCreatureTests(unittest.TestCase):
    def test_set_references_every_card_once(self) -> None:
        set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        includes = [
            line.removeprefix("include_file: ")
            for line in set_text.splitlines()
            if line.startswith("include_file: ")
        ]
        self.assertEqual(includes, sorted(EXPECTED_RULES))
        self.assertEqual(len(includes), len(set(includes)))

    def test_every_mse_card_uses_the_updated_rule_contract(self) -> None:
        stale_terms = ("bibliothèque", "cimetière", "champ de bataille", "défaussez-vous")
        for filename, expected_fragments in EXPECTED_RULES.items():
            with self.subTest(filename=filename):
                text = (PROJECT / filename).read_text(encoding="utf-8-sig")
                self.assertEqual(text.count("(1 - Résolution)"), 1)
                for fragment in expected_fragments:
                    self.assertIn(fragment, text)
                rule_text = text.split("\trule_text:\n", 1)[1].split("\tflavor_text:", 1)[0]
                for stale_term in stale_terms:
                    self.assertNotIn(stale_term, rule_text)
                self.assertNotIn("error-spelling", rule_text)
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

    def test_docs_mirror_the_updated_mse_rules(self) -> None:
        doc = DOC.read_text(encoding="utf-8-sig")
        self.assertEqual(doc.count("(1 - Résolution)"), len(EXPECTED_RULES))
        for filename, expected_fragments in EXPECTED_RULES.items():
            card_text = (PROJECT / filename).read_text(encoding="utf-8-sig")
            name = next(
                line.removeprefix("\tname: ")
                for line in card_text.splitlines()
                if line.startswith("\tname: ")
            )
            self.assertIn(f"### {name}", doc)
            for fragment in expected_fragments:
                markdown_fragment = fragment.replace("<b>", "**").replace("</b>", "**")
                self.assertIn(markdown_fragment, doc)

    def test_all_image_references_resolve(self) -> None:
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
