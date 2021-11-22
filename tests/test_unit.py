"""test_unit"""
__docformat__ = "numpy"

import unittest

from bot import bible, ESPN


class TestBible(unittest.TestCase):
    def test_get_books(self):
        books = bible.get_books()
        self.assertIn("Genesis", str(books))

    def test_get_chapters(self):
        chapters = bible.get_chapters("JHN")
        self.assertIn("3", str(chapters))

    def test_get_verse(self):
        verse = bible.get_verse("JHN", "3", "16")
        self.assertIn("God", str(verse))

    def test_get_text_to_verse(self):
        verse = bible.text_to_verse("@sportsbot john 3:16")
        self.assertIn("God", str(verse))


class TestESPN(unittest.TestCase):
    def test_get_stat(self):
        stats = ESPN.get_stat()
        self.assertIn("gameId", str(stats))

    def test_team_stats(self):
        team_stats = ESPN.team_stats()
        self.assertIn("abbrev", str(team_stats))

    def test_get_standings(self):
        standings = ESPN.get_standings()
        self.assertIn("\n", str(standings))

    def test_win_chance(self):
        win_chance = ESPN.win_chance()
        self.assertIn(" ", str(win_chance))
