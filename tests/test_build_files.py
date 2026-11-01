"""Linked build discovery must accept both compiler output suffixes safely."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))


class BuildFileTests(unittest.TestCase):
    def test_nef_and_elf_builds(self):
        from build_files import linked_image
        for suffix in ('.nef', '.elf'):
            with tempfile.TemporaryDirectory() as folder:
                (Path(folder) / ('main' + suffix)).touch()
                self.assertEqual(linked_image(folder), 'main' + suffix)

    def test_missing_or_ambiguous_outputs_are_rejected(self):
        from build_files import linked_image
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(SystemExit):
                linked_image(folder)
            (Path(folder) / 'main.nef').touch()
            (Path(folder) / 'main.elf').touch()
            with self.assertRaises(SystemExit):
                linked_image(folder)
