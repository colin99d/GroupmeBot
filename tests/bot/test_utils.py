import pytest
from bot import schemas
from bot import utils


def test_get_random():
    options = ["a", "b", "c", "d", "e"]
    option = utils.get_random(options)
    assert option in options


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_random_insult():
    insult = utils.random_insult(group_id=schemas.settings.TEST_GROUP_ID)
    assert "@" in insult


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_generate_card(mocker):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    mocker.patch("bot.utils.get_random", lambda x: x[0])
    utils.generate_card(group_id=schemas.settings.TEST_GROUP_ID)
    assert (
        "https://dbukjj6eu5tsf.cloudfront.net/sidearm.sites/bradley."
        in mock.call_args[0][0]
    )


@pytest.mark.skip
def test_generate_card_error(mocker):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    mocker.patch("bot.utils.get_random", lambda x: x[0])
    mock = mocker.patch("bot.utils.groupme.send_message")
    utils.generate_card(group_id=999999999999)
    mock.assert_called_once()
