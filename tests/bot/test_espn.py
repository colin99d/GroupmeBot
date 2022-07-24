import pytest
from bot import ESPN


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_get_stat():
    stats = ESPN.get_stat()
    assert len(stats) == 9


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_team_stats():
    team_stats = ESPN.team_stats()
    assert len(team_stats) == 10


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_get_standings():
    standings = ESPN.get_standings()
    assert "ame\tW\tL\nUUP?\t7 3\nHERB\t7 3\nROSS\t6 4\nFUCK\t6 4\nFOR" in standings


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_win_chance():
    win_chance = ESPN.win_chance()
    assert win_chance == "Winner is: UUP?"


def test_win_chance_less_than_nine(mocker):
    data = [
        {"abbrev": "hi", "points": 12, "record": {"overall": {"losses": 3, "wins": 4}}},
        {"abbrev": "bye", "points": 1, "record": {"overall": {"losses": 4, "wins": 3}}},
    ]
    mocker.patch("bot.ESPN.team_stats", return_value=data)
    win_chance = ESPN.win_chance()
    assert "Player's chance of winning:" in win_chance
