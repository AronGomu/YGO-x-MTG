from __future__ import annotations

import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "MSE_projects"
FRENCH_PROJECTS = PROJECTS / "French"
ARCHIVE_MANIFEST = ROOT / "FRENCH_ARCHIVE_SHA256SUMS"
INTENTIONAL_UNINCLUDED_CARDS = {
    "07_YGO_Staples_Xyz.mse-set": {"card aa zeus sky thunder"},
    "12_YGO_Necroz.mse-set": {
        "card dance princess of the nekroz",
        "card exa enforcer of the nekroz",
        "card great sorcerer of the nekroz",
        "card nekroz cycle",
        "card nekroz kaleidoscope",
        "card nekroz mirror",
        "card nekroz of brionac",
        "card nekroz of catastor",
        "card nekroz of clausolas",
        "card nekroz of decisive armor",
        "card nekroz of gungnir",
        "card nekroz of trishula",
        "card nekroz of unicore",
        "card nekroz of valkyrus",
        "card shurit strategist of the nekroz",
    },
}

FRENCH_MARKERS = re.compile(
    r"[àâçéèêëîïôùûüÿœæ]|"
    r"\b(?:votre|depuis|ciblez|carte|cartes|créature|créatures|détruisez|"
    r"exilez|piochez|défaussez|envoyez|renvoyez|mettez|cherchez|révélez|"
    r"choisissez|contrôlez|bibliothèque|cimetière|adversaire|coût|capacité|"
    r"lorsque|sacrifiez|jusqu’à)\b",
    re.IGNORECASE,
)


def archive_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def card_name(card_path: Path) -> str:
    text = card_path.read_text(encoding="utf-8-sig")
    return re.search(r"(?m)^\tname:\s*(.+)$", text).group(1).strip()  # type: ignore[union-attr]


def render_name(name: str) -> str:
    safe = name.replace(":", " -").replace('"', "'").replace("/", " - ")
    return "".join(char for char in safe if char not in "<>|?*") + ".png"


class EnglishSourceOfTruthTests(unittest.TestCase):
    def test_french_archive_matches_pinned_content_manifest(self) -> None:
        pinned: dict[str, str] = {}
        for line in ARCHIVE_MANIFEST.read_text(encoding="utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            pinned[relative] = digest

        roots = (
            ROOT / "MSE_projects/French",
            ROOT / "docs/French",
            ROOT / "rule_reviews/French",
            ROOT / "mse/French",
        )
        archived = {
            path.relative_to(ROOT).as_posix()
            for root in roots
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(set(pinned), archived)
        for relative, expected in pinned.items():
            with self.subTest(path=relative):
                self.assertEqual(archive_digest(ROOT / relative), expected)

    def test_canonical_manifests_and_renders_are_english_and_complete(self) -> None:
        for project in sorted(PROJECTS.glob("*.mse-set")):
            with self.subTest(project=project.name):
                set_text = (project / "set").read_text(encoding="utf-8-sig")
                self.assertIn("set_language: EN", set_text)
                self.assertIn("card_language: English", set_text)
                self.assertRegex(set_text, r"(?m)^\ttitle: YGO x MTG -- ")
                includes = re.findall(r"(?m)^include_file:\s*(.+)$", set_text)
                self.assertEqual(len(includes), len(set(includes)))
                for include in includes:
                    self.assertTrue((project / include).is_file(), include)
                all_cards = {path.name for path in project.glob("card *")}
                self.assertEqual(
                    all_cards - set(includes),
                    INTENTIONAL_UNINCLUDED_CARDS.get(project.name, set()),
                )
                expected_renders = {
                    render_name(card_name(project / include)) for include in includes
                }
                render_paths = list((project / "render").glob("*.png"))
                self.assertEqual(expected_renders, {path.name for path in render_paths})
                for render in render_paths:
                    with Image.open(render) as image:
                        image.verify()
                    with Image.open(render) as image:
                        self.assertGreater(image.width, 0)
                        self.assertGreater(image.height, 0)
                for card_path in project.glob("card *"):
                    text = card_path.read_text(encoding="utf-8-sig")
                    match = re.search(r"(?m)^\timage:\s*(.+)$", text)
                    if match and match.group(1).strip():
                        image_path = project / match.group(1).strip()
                        self.assertTrue(image_path.is_file(), image_path)
                        with Image.open(image_path) as image:
                            image.verify()

    def test_canonical_cards_have_no_french_prose_or_malformed_tags(self) -> None:
        for card_path in PROJECTS.glob("*.mse-set/card *"):
            with self.subTest(card=card_path):
                text = card_path.read_text(encoding="utf-8-sig")
                self.assertNotRegex(text, FRENCH_MARKERS)
                stack: list[str] = []
                for match in re.finditer(r"<(/?)([a-z][a-z0-9-]*)(?::[^>]*)?>", text, re.I):
                    closing, tag = match.group(1), match.group(2).lower()
                    if not closing:
                        stack.append(tag)
                    else:
                        self.assertTrue(stack, f"unexpected </{tag}>")
                        self.assertEqual(stack.pop(), tag)
                self.assertEqual(stack, [])

    def test_canonical_docs_and_reviews_are_english(self) -> None:
        canonical_docs = {
            path.name
            for path in (ROOT / "docs").glob("*.md")
            if not path.name.startswith("_")
        }
        self.assertIn("01_cube_overview.md", canonical_docs)
        self.assertNotIn("01_presentation_generale_regles_du_cube.md", canonical_docs)
        for name in canonical_docs:
            self.assertNotRegex(
                (ROOT / "docs" / name).read_text(encoding="utf-8-sig"),
                FRENCH_MARKERS,
            )

        reviews = {path.name for path in (ROOT / "rule_reviews").glob("*.md")}
        for name in reviews:
            self.assertNotRegex(
                (ROOT / "rule_reviews" / name).read_text(encoding="utf-8-sig"),
                FRENCH_MARKERS,
            )

    def test_card_workflows_protect_french_archives(self) -> None:
        for skill in (
            "add-ygo-card",
            "fix-mse-cards",
            "normalize-card-formatting",
            "update-card-from-ai",
        ):
            text = (ROOT / f".agents/skills/{skill}/SKILL.md").read_text(
                encoding="utf-8-sig"
            )
            self.assertIn("MSE_projects/French/", text)
            self.assertRegex(text, r"(?i)never edit|never write|reject any scope")

    def test_proxy_pdf_defaults_exclude_french_archive(self) -> None:
        script = ROOT / ".script/create_proxy_pdf.py"
        spec = importlib.util.spec_from_file_location("create_proxy_pdf", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        folders = module.discover_render_folders([])
        expected = sorted(
            (project / "render")
            for project in PROJECTS.glob("*.mse-set")
            if (project / "render").is_dir()
        )
        self.assertEqual(folders, expected)
        self.assertTrue(all("French" not in path.parts for path in folders))
        french_render = FRENCH_PROJECTS / "13_YGO_Spellbook.mse-set/render"
        with self.assertRaises(ValueError):
            module.discover_render_folders([french_render])

    def test_checked_in_proxy_pdfs_are_valid(self) -> None:
        expected = {
            "03_non_archetype_creatures_proxies.pdf",
            "09_non_archetype_non_creatures_proxies.pdf",
            "11_ygo_shaddoll_proxies.pdf",
            "13_spellbook_proxies.pdf",
            "burning_abyss_proxies.pdf",
            "trap_cards_proxies.pdf",
        }
        self.assertEqual(expected, {path.name for path in (ROOT / "print").glob("*.pdf")})
        for name in expected:
            data = (ROOT / "print" / name).read_bytes()
            self.assertTrue(data.startswith(b"%PDF-"), name)
            self.assertIn(b"%%EOF", data[-1024:], name)

    def test_legacy_sources_and_process_folder_are_absent(self) -> None:
        self.assertFalse((ROOT / "mse/set").exists())
        self.assertTrue((ROOT / "mse/French/set").is_file())
        self.assertFalse((ROOT / "5_processes").exists())
        for path in ROOT.rglob("*.md"):
            if "French" in path.parts:
                continue
            self.assertNotIn("5_processes", path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
