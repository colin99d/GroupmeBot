import pytest
from bot import bible
from bot import ESPN
from bot import groupme
from bot import market
from bot import schemas
from bot import utils


@pytest.mark.vcr
def test_get_books(recorder):
    books = bible.get_books()
    recorder.capture(books)


@pytest.mark.vcr
def test_get_chapters(recorder):
    chapters = bible.get_chapters("JHN")
    recorder.captrue(chapters)


@pytest.mark.vcr
def test_get_verse(recorder):
    verse = bible.get_verse("JHN", "3", "16")
    recorder.capture(verse)


@pytest.mark.vcr
def test_get_text_to_verse(recorder):
    verse = bible.text_to_verse("@sportsbot john 3:16")
    recorder.capture(verse)


@pytest.mark.vcr
def test_get_text_to_verse_error(recorder):
    verse = bible.text_to_verse("@sportsbot jonah 3:16")
    recorder.capture(verse)


@pytest.mark.vcr
def test_get_stat(recorder):
    stats = ESPN.get_stat()
    recorder.capture(stats)


@pytest.mark.vcr
def test_team_stats(recorder):
    team_stats = ESPN.team_stats()
    recorder.capture(team_stats)


@pytest.mark.vcr
def test_get_standings(recorder):
    standings = ESPN.get_standings()
    recorder.capture(standings)


@pytest.mark.vcr
def test_win_chance(recorder):
    win_chance = ESPN.win_chance()
    recorder.capture(win_chance)


def test_get_random():
    options = ["a", "b", "c", "d", "e"]
    option = utils.get_random(options)
    assert option in options


@pytest.mark.vcr
def test_random_insult():
    insult = utils.random_insult("Test string", schemas.settings.TEST_GROUP_ID)
    assert "@" in insult


def test_generate_card(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    utils.generate_card(None, schemas.settings.TEST_GROUP_ID)
    recorder.capture(mock.call_args)


@pytest.mark.vcr
def test_evan_voyager(recorder):
    text = market.evan_voyager()
    recorder.capture(text)


@pytest.mark.vcr
def test_chart_stock(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    market.chart_stock("@SportsBot stock TSLA", schemas.settings.TEST_GROUP_ID)
    recorder.capture(mock.call_args)


@pytest.mark.vcr
def test_chart_invalid(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_message", mock)
    market.chart_stock("@SportsBot stock TSLAXX", schemas.settings.TEST_GROUP_ID)
    recorder.capture(mock.call_args)


@pytest.mark.vcr
def test_send_image(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    groupme.send_image(
        "https://dbukjj6eu5tsf.cloudfront.net/gopsusports.com/images/2018/5/2/10251682.jpeg",
        schemas.settings.TEST_GROUP_ID,
    )
    recorder.capture(mock.call_args)


@pytest.mark.vcr
def test_send_message(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    groupme.send_message(
        "https://dbukjj6eu5tsf.cloudfront.net/gopsusports.com/images/2018/5/2/10251682.jpeg",
        schemas.settings.TEST_GROUP_ID,
    )


@pytest.mark.vcr
def test_remove_user(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("requests.post", mock)
    groupme.remove_user(schemas.settings.TEST_GROUP_ID, "29762584")
    recorder.capture(mock.call_args)


@pytest.mark.vcr
def test_group_info():
    post = groupme.group_info(schemas.settings.TEST_GROUP_ID)
    assert post.status_code == 200


@pytest.mark.vcr
def test_list_groups():
    post = groupme.list_groups()
    assert post.status_code == 200


@pytest.mark.vcr
def test_add_user(mocker, recorder):
    mock = mocker.Mock()
    mocker.patch("requests.post", mock)
    groupme.add_user(schemas.settings.TEST_GROUP_ID, "29762584")
    recorder.capture(mock.call_args)
