"""Market"""
__docformat__ = "numpy"

import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt

from . import groupme

matplotlib.use("Agg")


def evan_voyager(*args) -> str:
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info["currentPrice"])
    d = (price - 16) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d), 2)
    return f"Evan has {t} ${d} from Voyager."


def chart_stock(text: str, group: str):
    ticker = text.split(" ")[-1]
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hist.index, hist["Close"], color="tab:blue", label="Portfolio")
    ax.yaxis.set_major_formatter("${x:1.2f}")
    ax.set_title(f"Ending prices for {ticker.upper()}")
    fig.savefig("images/chart.png", format="png")
    groupme.send_image("chart.png", group)
