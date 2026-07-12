from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "MSE_projects" / "11_YGO_Shaddoll.mse-set"
DOC = ROOT / "docs" / "11_archetype_shaddoll.md"

EXPECTED_NAMES = {
    "El Shaddoll - Anoyatyllis",
    "El Shaddoll - Apkallone",
    "El Shaddoll - Construct",
    "El Shaddoll - Fusion",
    "El Shaddoll - Grysta",
    "El Shaddoll - Shekhinaga",
    "El Shaddoll - Wendigo",
    "El Shaddoll - Winda",
    "Hel Shaddoll - Hollow",
    "Nael Shaddoll - Ariel",
    "Puru Shaddoll - Aeon",
    "Qad Shaddoll - Keios",
    "Ree Shaddoll - Wendi",
    "Resh Shaddoll - Incarnation",
    "Shaddoll - Beast",
    "Shaddoll - Core",
    "Shaddoll - Dragon",
    "Shaddoll - Falco",
    "Shaddoll - Fusion",
    "Shaddoll - Hedgehog",
    "Shaddoll - Hound",
    "Shaddoll - Schism",
    "Curse of the Shadow Prison",
    "Sinister Shadow Games",
    "Shaddoll - Squamata",
}


def field(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\t{re.escape(key)}:[ \t]*(.*)$", text)
    return match.group(1).strip() if match else ""


def rules(text: str) -> list[str]:
    match = re.search(
        r"(?ms)^\trule_text:\n(?P<body>(?:\t\t.*\n)+?)(?=^\tflavor_text:)", text
    )
    if not match:
        return []
    return [line[2:] for line in match.group("body").splitlines()]


def markdown_rule(line: str) -> str:
    line = re.sub(r"<i-auto>(.*?)</i-auto>", r"\1", line)
    line = re.sub(r"<b>(.*?)</b>", r"**\1**", line)
    line = re.sub(r"<i>(.*?)</i>", r"*\1*", line)
    return line


class ShaddollCardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.set_text = (PROJECT / "set").read_text(encoding="utf-8-sig")
        cls.includes = [
            line.split(":", 1)[1].strip()
            for line in cls.set_text.splitlines()
            if line.startswith("include_file:")
        ]
        cls.cards = {
            include: (PROJECT / include).read_text(encoding="utf-8-sig")
            for include in cls.includes
        }
        cls.doc = DOC.read_text(encoding="utf-8-sig")

    def test_manifest_is_complete_sorted_and_has_no_orphan_cards(self) -> None:
        self.assertEqual(25, len(self.includes))
        self.assertEqual(len(self.includes), len(set(self.includes)))
        names = [field(self.cards[include], "name") for include in self.includes]
        self.assertEqual(sorted(names, key=str.casefold), names)
        self.assertEqual(EXPECTED_NAMES, set(names))
        self.assertEqual(set(self.includes), {path.name for path in PROJECT.glob("card *")})

    def test_images_and_collector_numbers_resolve(self) -> None:
        referenced_images: set[str] = set()
        for index, include in enumerate(self.includes, 1):
            text = self.cards[include]
            with self.subTest(card=field(text, "name")):
                image = field(text, "image")
                self.assertTrue(image)
                self.assertTrue((PROJECT / image).is_file(), image)
                referenced_images.add(image)
                expected = f"{index:03d}/025 C"
                for key in ("card_code_text", "card_code_text_2", "card_code_text_3"):
                    self.assertEqual(expected, field(text, key))

        local_images = {
            path.relative_to(PROJECT).as_posix()
            for path in (PROJECT / "mse_images").glob("*")
            if path.is_file()
        }
        self.assertEqual(local_images, {path for path in referenced_images if path.startswith("mse_images/")})

    def test_frames_follow_super_type(self) -> None:
        for text in self.cards.values():
            name = field(text, "name")
            super_type = field(text, "super_type")
            with self.subTest(card=name):
                if ">Fusion Creature<" in super_type:
                    self.assertEqual("genevensis-00-main", field(text, "stylesheet"))
                    self.assertEqual("2022-02-22", field(text, "stylesheet_version"))
                    self.assertRegex(rules(text)[0], r"^<i>.+</i>$")
                else:
                    self.assertEqual("sevenhalf", field(text, "stylesheet"))
                    self.assertEqual("2024-05-30", field(text, "stylesheet_version"))

    def test_rules_use_current_formatting(self) -> None:
        forbidden = re.compile(
            r"\b(?:bibliothèque|cimetière)\b|On Send GY(?!D)|\?{2,}|\b(?:Declenchable|creature Blue)\b",
            re.IGNORECASE,
        )
        for text in self.cards.values():
            name = field(text, "name")
            card_rules = rules(text)
            with self.subTest(card=name):
                self.assertTrue(card_rules)
                for index, line in enumerate(card_rules):
                    self.assertNotRegex(line, forbidden)
                    if index == 0 and line.startswith("<i>"):
                        continue
                    self.assertRegex(line, r"^<i-auto>\(\d+ - .+\)</i-auto> ")

    def test_mse_rules_are_mirrored_in_numbered_doc(self) -> None:
        sections = {
            match.group("cube").strip(): match.group("body")
            for match in re.finditer(
                r"(?ms)^## [^\n]+ => (?P<cube>[^\n]+)\n(?P<body>.*?)(?=\n---|\Z)",
                self.doc,
            )
        }
        self.assertEqual(EXPECTED_NAMES, set(sections))
        for text in self.cards.values():
            name = field(text, "name")
            with self.subTest(card=name):
                section = sections[name]
                self.assertIn(f"**Coût :** {{{field(text, 'casting_cost')}}}".replace("{1B}", "{1}{B}").replace("{2U}", "{2}{U}").replace("{2W}", "{2}{W}").replace("{2G}", "{2}{G}").replace("{2R}", "{2}{R}"), section)
                for line in rules(text):
                    self.assertIn(markdown_rule(line), section)

    def test_render_names_match_card_names_exactly(self) -> None:
        expected = {
            f"{field(text, 'name')}.png"
            for text in self.cards.values()
        }
        actual = {path.name for path in (PROJECT / "render").glob("*.png")}
        self.assertEqual(expected, actual)

    def test_approved_anoyatyllis_and_aeon_mechanics_are_preserved(self) -> None:
        by_name = {field(text, "name"): text for text in self.cards.values()}
        anoyatyllis = by_name["El Shaddoll - Anoyatyllis"]
        self.assertIn("depuis une main ou un GYD", anoyatyllis)
        self.assertIn("<b>On Send GYD</b>", anoyatyllis)
        self.assertIn("Ciblez 1 carte", anoyatyllis)
        self.assertNotIn("Soft", "\n".join(rules(anoyatyllis)))

        aeon = by_name["Puru Shaddoll - Aeon"]
        self.assertEqual("0", field(aeon, "casting_cost"))
        self.assertIn(">Trap Instant<", field(aeon, "super_type"))
        self.assertIn("Ciblez 1 créature", aeon)
        self.assertIn("jusqu’à la fin du tour", aeon)
        self.assertIn("Au début de l’étape de fin", aeon)
        self.assertNotIn("Si vous faites ainsi", aeon)


if __name__ == "__main__":
    unittest.main()
