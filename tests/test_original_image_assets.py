from __future__ import annotations

import hashlib
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MSE_PROJECTS = REPO_ROOT / "MSE_projects"
ORIGINAL_IMAGES = REPO_ROOT / "assets" / "original_images"
sys.path.insert(0, str(REPO_ROOT / ".script"))

from original_image_assets import archetype_folder, original_image_path


class OriginalImageAssetTests(unittest.TestCase):
    def test_original_art_is_centralized_outside_mse_projects(self) -> None:
        self.assertTrue(ORIGINAL_IMAGES.is_dir())
        for project in MSE_PROJECTS.glob("*.mse-set"):
            with self.subTest(project=project.name):
                self.assertFalse((project / "original_images").exists())
                self.assertFalse((project / "images").exists())

    def test_library_has_no_duplicate_source_files(self) -> None:
        files = sorted(path for path in ORIGINAL_IMAGES.rglob("*") if path.is_file())
        self.assertTrue(files)
        hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in files]
        self.assertEqual(len(hashes), len(set(hashes)))
        for path in files:
            with self.subTest(path=path):
                self.assertEqual(path.parent.parent, ORIGINAL_IMAGES)
                self.assertEqual(path.suffix.lower(), ".jpg")

    def test_actual_ygo_archetypes_override_cube_grouping(self) -> None:
        expected = (
            ORIGINAL_IMAGES
            / "burning_abyss"
            / "beatrice_lady_of_the_eternal.jpg"
        )
        self.assertTrue(expected.is_file())
        self.assertTrue(
            (ORIGINAL_IMAGES / "d_d" / "d_d_crow.jpg").is_file()
        )
        self.assertTrue(
            (ORIGINAL_IMAGES / "non_archetype" / "preparation_of_rites.jpg").is_file()
        )
        self.assertTrue(
            (ORIGINAL_IMAGES / "shaddoll" / "el_shaddoll_winda_variant_2.jpg").is_file()
        )

    def test_path_helper_uses_api_archetype_metadata(self) -> None:
        card = {"name": "D.D. Crow", "archetype": "D.D."}
        self.assertEqual(archetype_folder(card), "d_d")
        self.assertEqual(
            original_image_path(card),
            ORIGINAL_IMAGES / "d_d" / "d_d_crow.jpg",
        )
        self.assertEqual(archetype_folder({"name": "Ash Blossom"}), "non_archetype")

    def test_mse_cards_only_reference_project_local_images(self) -> None:
        for project in MSE_PROJECTS.glob("*.mse-set"):
            for card_file in project.glob("card *"):
                text = card_file.read_text(encoding="utf-8-sig", errors="replace")
                match = re.search(r"(?m)^\s*image:\s*(.*?)\s*$", text)
                if not match or not match.group(1):
                    continue
                image_value = match.group(1)
                with self.subTest(card=card_file):
                    self.assertFalse(image_value.startswith("assets/"))
                    self.assertFalse(image_value.startswith("images/"))
                    self.assertNotIn("original_images/", image_value)
                    self.assertTrue((project / image_value).is_file())


if __name__ == "__main__":
    unittest.main()
