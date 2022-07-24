import pytest
from bot import helpers
from tests import helpers as thelps


@pytest.mark.parametrize("option", helpers.message_dict.keys())
def test_webhook(option, client, mock_actions, mocker):
    del mock_actions
    if option != "help":
        mock = mocker.patch("bot.helpers.groupme.send_message")
        data = thelps.get_post(option)
        response = client.post("/", json=data)
        print(response.json())
        assert response.status_code == 200
        mock.assert_called_once()


def test_language_detector(mocker, client):
    mock1 = mocker.patch("bot.helpers.groupme.send_message")
    mock2 = mocker.patch("bot.helpers.groupme.remove_user")
    data = thelps.get_post("retard")
    client.post("/", json=data)
    mock1.assert_called_once()
    mock2.assert_called_once()


def test_help_message(mocker, client):
    mock1 = mocker.patch("bot.helpers.groupme.send_message")
    data = thelps.get_post("help")
    client.post("/", json=data)
    assert mock1.call_args[0][0] == "https://mygroupmetestbot.herokuapp.com/"


def test_invalid_message(mocker, client):
    mock1 = mocker.patch("bot.helpers.groupme.send_message")
    data = thelps.get_post("beepboop")
    client.post("/", json=data)
    assert (
        mock1.call_args[0][0] == "Invalid command. Call 'help' for a list of commands"
    )


def test_docs(client):
    response = client.get("/")
    for item in helpers.message_dict:
        if item != "help":
            assert item.title() in response.text


def test_messages(client):
    response = client.get("/messages")
    assert response.status_code == 200
