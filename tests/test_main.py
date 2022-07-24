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
