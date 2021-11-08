"""Bot utils"""
__docformat__ = "numpy"

import html
import json
import os
import pathlib
from random import randint
from typing import List, Dict

import requests
import yfinance as yf

from . import data

base = "https://api.groupme.com/v3"
end = "?token=85w8CudYavVwkN7YAdOQwSyzXyCYDx7SV9aLBoRL"


def get_random(lst):
    amount = len(lst)
    rnd = randint(0, amount - 1)
    return lst[rnd]


def get_bot_id(group_id: str) -> str:
    if group_id == "69502628":
        return "5e6fccada121999d1dd6759d7a"
    elif group_id == "46166401":
        return "d1d19ce1822d3080e157027858"
    else:
        return ""


def upload_image(image: str) -> requests.Response:
    url = "https://image.groupme.com/pictures"
    headers = {
        "Content-Type": "image/jpeg",
        "X-Access-Token": "85w8CudYavVwkN7YAdOQwSyzXyCYDx7SV9aLBoRL",
    }
    path_string = pathlib.Path(__file__).parent.parent.resolve()
    path = os.path.join(path_string, "images", image)
    data = open(path, "rb").read()
    return requests.post(url, data=data, headers=headers)


def send_message(message: str, group_id: str) -> requests.Response:
    mid = "/bots/post"
    bot_id = get_bot_id(group_id)
    return requests.post(url=f"{base+mid}?bot_id={bot_id}&text={message}")


def send_image(image: str, group_id: str, text: str = None) -> requests.Response:
    image_url = upload_image(image).json()["payload"]["picture_url"]
    mid = "/bots/post"
    bot_id = get_bot_id(group_id)
    data = {
        "bot_id": bot_id,
        "text": text,
        "attachments": [{"type": "image", "url": image_url}],
    }
    return requests.post(base + mid + end, data=json.dumps(data))


def get_members(group: str) -> List[Dict[str, str]]:
    mid = f"/groups/{group}"
    response = requests.get(base + mid + end)
    members = response.json()["response"]["members"]
    return members


def get_id(group: str, user: str) -> str:
    members = get_members(group)
    result = list(filter(lambda x: int(x["user_id"]) == int(user), members))
    return result[0]["id"]


def evan_voyager(*args) -> str:
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info["currentPrice"])
    d = (price - 16) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d), 2)
    return f"Evan has {t} ${d} from Voyager."


def remove_user(group: str, user: str) -> None:
    id = get_id(group, user)
    mid = f"/groups/{group}/members/{id}/remove"
    data = {"membership_id": id}
    requests.post(base + mid + end, data=json.dumps(data))


def random_insult(_, group: str) -> str:
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=text"
    )
    data = html.unescape(response.text)
    insult = data[0].lower() + data[1:]
    members = get_members(group)
    name = get_random(members)["nickname"]
    return f"@{name} {insult}"


def generate_card(_, group_id):
    selection = get_random(list(data.players))
    p = data.players[selection]
    send_image(p["image"], group_id, selection)
    strengths: str = "".join([x + "\n" for x in p["Strengths"]])
    weaknesses: str = "".join([x + "\n" for x in p["Weaknesses"]])
    return f"{p['Description']}\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"


# Does not work, recipient_id causes issues
def direct_message(group, user):
    id = get_id(group, user)
    mid = "/direct_messages"
    cap = f"&source_guid=GUID&recipient_id={id}"
    data = {
        "direct_message": {
            "source_guid": "GUID",
            "recipient_id": f"{id}",
            "text": "Do you put out?",
        }
    }
    data = requests.post(base + mid + end + cap, data=json.dumps(data))
    print(data.text)
