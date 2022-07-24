import pytest
from bot import helpers
from bot import schemas


def create_request(option):
    return {
        "attachments": [],
        "avatar_url": "https://i.groupme.com/1024x1024.jpeg.c64d4fc5aeca45cb9fd2c1ca054fc22d",
        "created_at": 1632929238,
        "group_id": schemas.settings.TEST_GROUP_ID,
        "id": "163292923878111513",
        "name": "Colin Delahunty",
        "sender_id": "29762584",
        "sender_type": "user",
        "source_guid": "baac853e03cdf5d1d1ff77f105711ef3",
        "system": False,
        "text": f"@sportsbot {option}",
        "user_id": "29762584",
    }


def return_message(**kwargs):
    del kwargs
    return "A friendly message"


@pytest.fixture(scope="function")
def mock_actions(mocker):
    new_dict = {
        x: return_message
        for x in [
            "bible",
            "scores",
            "winner",
            "stock",
            "voyager",
            "insult",
            "card",
            "stats",
        ]
    }
    mocker.patch("bot.helpers.message_dict", new_dict)


@pytest.mark.parametrize("option", helpers.message_dict.keys())
def test_webhook(option, client, mock_actions, mocker):
    if option != "help":
        mock = mocker.patch("bot.helpers.groupme.send_message")
        data = create_request(option)
        response = client.post("/", json=data)
        print(response.json())
        assert response.status_code == 200
        mock.assert_called_once()
