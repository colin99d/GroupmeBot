import pytest
from bot import schemas, utils
from tests import helpers as thelps


def test_get_random():
    options = ["a", "b", "c", "d", "e"]
    option = utils.get_random(options)
    assert option in options


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_random_insult():
    insult = utils.random_insult(group_id=schemas.settings.TEST_GROUP_ID)
    assert "@" in insult


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
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
    data = {
        "Test": {
            "Strengths": ["1"],
            "Weaknesses": ["2"],
            "Description": "3",
        }
    }
    mocker.patch("bot.utils.json.load", return_value=data)
    mocker.patch("bot.utils.get_random", return_value="Test")
    mock = mocker.patch("bot.utils.groupme.send_message")
    utils.generate_card(group_id=schemas.settings.TEST_GROUP_ID)
    mock.assert_called_once()


def test_handle_stats(db):
    data = thelps.get_post("Hello")
    schema = schemas.Message(**data)
    utils.add_post(db, schema)
    value = utils.handle_stats(group_id=schemas.settings.TEST_GROUP_ID, db=db)
    assert value
