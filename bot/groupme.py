"""Groupme"""
__docformat__ = "numpy"

import json
import io
import os
import pathlib
import urllib.request as urllib
from typing import List, Dict

import requests
from .schemas import settings


base = "https://api.groupme.com/v3"
TOKEN = settings.GROUPME_TOKEN
end = f"?token={TOKEN}"

group_to_bot = {
    settings.TEST_GROUP_ID: settings.TEST_GROUP_BOT,
    settings.MAIN_GROUP_ID: settings.MAIN_GROUP_BOT,
}


def upload_image(image: str, local: bool) -> requests.Response:
    url = "https://image.groupme.com/pictures"
    headers = {
        "Content-Type": "image/jpeg",
        "X-Access-Token": "85w8CudYavVwkN7YAdOQwSyzXyCYDx7SV9aLBoRL",
    }
    if local:
        path_string = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path_string, image)
        return requests.post(url, data=open(path, "rb").read(), headers=headers)
    data = urllib.urlopen(image)
    return requests.post(url, data=io.BytesIO(data.read()), headers=headers)


def send_message(message: str, group_id: str) -> requests.Response:
    mid = "/bots/post"
    bot_id = group_to_bot[group_id]
    return requests.post(url=f"{base+mid}?bot_id={bot_id}&text={message}")


def send_image(
    image: str, group_id: str, text: str = None, local: bool = False
) -> requests.Response:
    image_url = upload_image(image, local).json()["payload"]["picture_url"]
    mid = "/bots/post"
    bot_id = group_to_bot[group_id]
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


def remove_user(group: str, user: str) -> None:
    user_id = get_id(group, user)
    mid = f"/groups/{group}/members/{user_id}/remove"
    data = {"membership_id": user_id}
    requests.post(base + mid + end, data=json.dumps(data))


def group_info(group: str):
    mid = f"/groups/{group}"
    data = {"id": group}
    return requests.get(base + mid + end, data=json.dumps(data))


def list_groups():
    mid = "/groups"
    return requests.get(base + mid + end)


def add_user(group: str, packet):
    mid = f"/groups/{group}/members/add"
    requests.post(base + mid + end, data=json.dumps(packet))
