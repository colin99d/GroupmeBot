import pytest
from bot import market
from bot import schemas


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_evan_voyager():
    text = market.evan_voyager()
    assert text == "Evan has lost $4788.42 from Voyager."


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_chart_stock(mocker):
    mock = mocker.Mock()
    mocker.patch("bot.groupme.send_image", mock)
    market.chart_stock(
        text="@SportsBot stock TSLA", group_id=schemas.settings.TEST_GROUP_ID
    )
    assert mock.call_args[0][0] == "chart.png"


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path"])
def test_chart_invalid(mocker, capsys):
    mocker.patch("bot.groupme.send_message")
    market.chart_stock(
        text="@SportsBot stock TSLAXX", group_id=schemas.settings.TEST_GROUP_ID
    )
    captured = capsys.readouterr()
    assert "TSLAXX: No data found, symbol may be delisted" in captured.out
