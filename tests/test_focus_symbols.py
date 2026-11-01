"""Renamed game functions must keep the frontend's stable probe names."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))


class FocusSymbolTests(unittest.TestCase):
    def test_original_or_renamed_functions_keep_the_requested_name(self):
        from focus_symbols import find_focus
        for actual in ('sub_0203D264', 'Task_StartMenu_WaitSaveAppOpen'):
            functions = [('main', 0x0203CFFC, 34, actual)]
            self.assertEqual(find_focus(functions, 'sub_0203D264'),
                             [('sub_0203D264', 'main', 0x0203CFFC)])

    def test_all_renames_and_unknown_names(self):
        from focus_symbols import ALIASES, find_focus
        for canonical, renamed in ALIASES.items():
            self.assertEqual(find_focus([('overlay', 1234, 8, renamed)], canonical),
                             [(canonical, 'overlay', 1234)])
        self.assertEqual(find_focus([], 'missing'), [])
        self.assertEqual(find_focus([('main', 42, 8, 'unchanged')], 'unchanged'),
                         [('unchanged', 'main', 42)])

    def test_original_name_takes_precedence(self):
        from focus_symbols import find_focus
        functions = [('main', 100, 8, 'sub_0203D264'),
                     ('main', 200, 8, 'Task_StartMenu_WaitSaveAppOpen')]
        self.assertEqual(find_focus(functions, 'sub_0203D264'),
                         [('sub_0203D264', 'main', 100)])
