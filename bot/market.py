"""Market"""
__docformat__ = "numpy"

from typing import Optional
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt

from . import groupme

matplotlib.use("Agg")


def evan_voyager(**kwargs) -> str:
    del kwargs
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info["currentPrice"])
    d = (price - 16.23) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d), 2)
    return f"Evan has {t} ${d} from Voyager."


def chart_stock(**kwargs) -> Optional[str]:
    text = kwargs["text"]
    group = kwargs["group_id"]
    ticker = text.split(" ")[-1]
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    if hist["Close"].empty:
        return f"{ticker.upper()} is not a valid ticker."
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hist.index, hist["Close"], color="tab:blue", label="Portfolio")
    ax.yaxis.set_major_formatter("${x:1.2f}")
    ax.set_title(f"Ending prices for {ticker.upper()}")
    fig.savefig("chart.png", format="png")
    groupme.send_image("chart.png", group, "", True)
    return None
