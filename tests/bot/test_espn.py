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
