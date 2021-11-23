"""test_unit"""
__docformat__ = "numpy"

from unittest.mock import patch
import unittest
import os

import vcr

from bot import bible, ESPN, utils, market, groupme
from tests.helpers import check_print
from app import app


def get_post(message):
    return {
        "attachments": [],
        "avatar_url": "https://i.groupme.com/1024x1024.jpeg.c64d4fc5aeca45cb9fd2c1ca054fc22d",
        "created_at": "1632929238",
        "group_id": "69502628",
        "id": "163292923878111513",
        "name": "Colin Delahunty",
        "sender_id": "29762584",
        "sender_type": "user",
        "source_guid": "baac853e03cdf5d1d1ff77f105711ef3",
        "system": False,
        "text": f"@SportsBot {message}",
        "user_id": "29762584",
    }


def return_vals(*args, **_):
    for arg in args:
        print(arg)


class TestBible(unittest.TestCase):
    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_bible/test_get_books.yaml",
        record_mode="new_episodes",
    )
    def test_get_books(self):
        books = bible.get_books()
        self.assertIn("Genesis", str(books))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_bible/test_get_chapters.yaml",
        record_mode="new_episodes",
    )
    def test_get_chapters(self):
        chapters = bible.get_chapters("JHN")
        self.assertIn("3", str(chapters))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_bible/test_get_verse.yaml",
        record_mode="new_episodes",
    )
    def test_get_verse(self):
        verse = bible.get_verse("JHN", "3", "16")
        self.assertIn("God", str(verse))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_bible/test_text_to_verse.yaml",
        record_mode="new_episodes",
    )
    def test_get_text_to_verse(self):
        verse = bible.text_to_verse("@sportsbot john 3:16")
        self.assertIn("God", str(verse))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_bible/test_text_to_verse_error.yaml",
        record_mode="new_episodes",
    )
    def test_get_text_to_verse_error(self):
        verse = bible.text_to_verse("@sportsbot jonah 3:16")
        self.assertIn("Could not find verse", str(verse))


class TestESPN(unittest.TestCase):
    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_ESPN/test_get_stat.yaml",
        record_mode="new_episodes",
    )
    def test_get_stat(self):
        stats = ESPN.get_stat()
        self.assertIn("gameId", str(stats))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_ESPN/test_team_stats.yaml",
        record_mode="new_episodes",
    )
    def test_team_stats(self):
        team_stats = ESPN.team_stats()
        self.assertIn("abbrev", str(team_stats))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_ESPN/test_get_standings.yaml",
        record_mode="new_episodes",
    )
    def test_get_standings(self):
        standings = ESPN.get_standings()
        self.assertIn("\n", str(standings))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_ESPN/test_win_chance.yaml",
        record_mode="new_episodes",
    )
    def test_win_chance(self):
        win_chance = ESPN.win_chance()
        self.assertIn(" ", str(win_chance))


class TestFlask(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

        with app.app_context():
            with app.test_client() as client:
                self.client = client

    def test_get_home(self):
        rv = self.client.get("/")
        self.assertIn("Winner", str(rv.data))

    @check_print(assert_in="help")
    @patch("bot.groupme.send_message", side_effect=return_vals)
    def test_invalid_selection(self, _):
        data = get_post("efwffeew")
        self.client.post("/", json=data)

    @check_print(assert_in="R-word")
    @patch("bot.groupme.send_message", side_effect=return_vals)
    @patch("bot.groupme.remove_user", side_effect=return_vals)
    def test_saying_retard(self, *_):
        data = get_post("retard")
        self.client.post("/", json=data)

    @check_print(assert_in="https://mygroupmetestbot.herokuapp.com/")
    @patch("bot.groupme.send_message", side_effect=return_vals)
    def test_help(self, _):
        data = get_post("help")
        self.client.post("/", json=data)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_flask/test_bible.yaml",
        record_mode="new_episodes",
    )
    @check_print(assert_in="God")
    @patch("bot.groupme.send_message", side_effect=return_vals)
    def test_bible(self, _):
        data = get_post("bible john 3:16")
        self.client.post("/", json=data)


class TestUtils(unittest.TestCase):
    def test_get_random(self):
        options = ["a", "b", "c", "d", "e"]
        option = utils.get_random(options)
        self.assertIn(option, options)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_utils/test_random_insult.yaml",
        record_mode="new_episodes",
    )
    def test_random_insult(self):
        insult = utils.random_insult("Test string", os.getenv("TEST_GROUP_ID"))
        self.assertIn("@", insult)

    @check_print(assert_in="Strength")
    @patch("bot.groupme.send_image", side_effect=return_vals)
    def test_generate_card(self, _):
        utils.generate_card(None, os.getenv("TEST_GROUP_ID"))


class TestMarket(unittest.TestCase):
    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_market/test_evan_voyager.yaml",
        record_mode="new_episodes",
    )
    def test_evan_voyager(self):
        text = market.evan_voyager()
        self.assertIn("Evan", text)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_market/test_chart_stock.yaml",
        record_mode="new_episodes",
    )
    @check_print(assert_in="chart.png")
    @patch("bot.groupme.send_image", side_effect=return_vals)
    def test_chart_stock(self, _):
        market.chart_stock("@SportsBot stock TSLA", os.getenv("TEST_GROUP_ID"))

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_market/test_chart_invalid.yaml",
        record_mode="new_episodes",
    )
    @check_print(assert_in="No data found")
    @patch("bot.groupme.send_message", side_effect=return_vals)
    def test_chart_invalid(self, _):
        market.chart_stock("@SportsBot stock TSLAXX", os.getenv("TEST_GROUP_ID"))


class TestGroupme(unittest.TestCase):
    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_send_image.yaml",
        record_mode="new_episodes",
    )
    def test_send_image(self):
        post = groupme.send_image("AlecH.jpeg", os.getenv("TEST_GROUP_ID"))
        self.assertEqual(post.status_code, 202)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_send_message.yaml",
        record_mode="new_episodes",
    )
    def test_send_message(self):
        post = groupme.send_message("AlecH.jpeg", os.getenv("TEST_GROUP_ID"))
        self.assertEqual(post.status_code, 202)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_remove_user.yaml",
        record_mode="new_episodes",
    )
    @check_print(assert_in="/members/")
    @patch("requests.post", side_effect=return_vals)
    def test_remove_user(self, _):
        groupme.remove_user(os.getenv("TEST_GROUP_ID"), "29762584")

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_group_info.yaml",
        record_mode="new_episodes",
    )
    def test_group_info(self):
        post = groupme.group_info(os.getenv("TEST_GROUP_ID"))
        self.assertEqual(post.status_code, 200)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_list_groups.yaml",
        record_mode="new_episodes",
    )
    def test_list_groups(self):
        post = groupme.list_groups()
        self.assertEqual(post.status_code, 200)

    @vcr.use_cassette(
        "tests/cassettes/test_unit/test_groupme/test_add_user.yaml",
        record_mode="new_episodes",
    )
    @check_print(assert_in="/members/add")
    @patch("requests.post", side_effect=return_vals)
    def test_add_user(self, _):
        groupme.add_user(os.getenv("TEST_GROUP_ID"), "29762584")
