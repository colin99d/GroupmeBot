import pytest
from bot import groupme
from bot import schemas


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_send_image(mocker):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    groupme.send_image(
        "https://dbukjj6eu5tsf.cloudfront.net/gopsusports.com/images/2018/5/2/10251682.jpeg",
        schemas.settings.TEST_GROUP_ID,
    )


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_send_message(mocker):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    groupme.send_message(
        "https://dbukjj6eu5tsf.cloudfront.net/gopsusports.com/images/2018/5/2/10251682.jpeg",
        schemas.settings.TEST_GROUP_ID,
    )


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_remove_user(mocker):
    mock = mocker.Mock()
    mocker.patch("requests.post", mock)
    groupme.remove_user(schemas.settings.TEST_GROUP_ID, "29762584")
    assert "https://api.groupme.com/v3/groups/" in mock.call_args[0][0]


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_group_info():
    post = groupme.group_info(schemas.settings.TEST_GROUP_ID)
    assert post.status_code == 200


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_list_groups():
    post = groupme.list_groups()
    assert post.status_code == 200


@pytest.mark.vcr(match_on=["method", "scheme", "port"])
def test_add_user(mocker):
    mock = mocker.Mock()
    mocker.patch("requests.post", mock)
    groupme.add_user(schemas.settings.TEST_GROUP_ID, "29762584")
    assert "https://api.groupme.com/v3/groups/" in mock.call_args[0][0]
