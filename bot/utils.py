"""Bot utils"""
__docformat__ = "numpy"

import html
from random import randint

import requests
import yfinance as yf

from . import data, groupme


def get_random(lst):
    amount = len(lst)
    rnd = randint(0, amount - 1)
    return lst[rnd]


def evan_voyager(*args) -> str:
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info["currentPrice"])
    d = (price - 16) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d), 2)
    return f"Evan has {t} ${d} from Voyager."


def random_insult(_, group: str) -> str:
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=text"
    )
    data = html.unescape(response.text)
    insult = data[0].lower() + data[1:]
    members = groupme.get_members(group)
    name = get_random(members)["nickname"]
    return f"@{name} {insult}"


def generate_card(_, group_id):
    selection = get_random(list(data.players))
    p = data.players[selection]
    strengths: str = "".join([x + "\n" for x in p["Strengths"]])
    weaknesses: str = "".join([x + "\n" for x in p["Weaknesses"]])
    selection += (
        f"\n{p['Description']}\n\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"
    )
    groupme.send_image(p["image"], group_id, selection)


def nathan(*args):
    lines = []
    with open("bot/abstinence.txt") as file:
        for line in file:
            lines.append(line)
    selection = get_random(lines)
    response = "Nathaniel,\n\n Abstinence is hard. When you are in a stick situation"
    response += f" tell the girl: {selection}"
    print(response)
    return response
