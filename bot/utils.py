"""Bot utils"""
__docformat__ = "numpy"
import json
from urllib.error import HTTPError

import html
from random import randint
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import requests

from . import groupme, models, schemas


def get_random(lst):
    amount = len(lst)
    rnd = randint(0, amount - 1)
    return lst[rnd]


def random_insult(**kwargs) -> str:
    group = kwargs["group_id"]
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=text"
    )
    data = html.unescape(response.text)
    insult = data[0].lower() + data[1:]
    members = groupme.get_members(group)
    name = get_random(members)["nickname"]
    return f"@{name} {insult}"


def generate_card(**kwargs):
    group_id = kwargs["group_id"]
    with open("bot/data/players.json", encoding="utf-8") as json_file:
        players = json.load(json_file)
    selection = get_random(list(players))
    p = players[selection]
    strengths: str = "".join([x + "\n" for x in p["Strengths"]])
    weaknesses: str = "".join([x + "\n" for x in p["Weaknesses"]])
    selection += (
        f"\n{p['Description']}\n\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"
    )
    try:
        groupme.send_image(p["image"], group_id, selection)
    except HTTPError:
        groupme.send_message(selection, group_id)


def handle_stats(**kwargs):
    group_id = kwargs["group_id"]
    db = kwargs["db"]
    query = (
        db.query(models.Post.name, func.count(models.Post.name).label("name_count"))
        .group_by(models.Post.name)
        .filter_by(group_id=group_id)
        .order_by(desc("name_count"))
    )
    string = "Messages by user:"
    for item in query.all():
        string += f"\n{item[0]} {item[1]}"
    return string


def add_post(db: Session, body: schemas.Message):
    message = models.Post(
        avatar_url=body.avatar_url.strip(),
        created_at=body.created_at,
        group_id=body.group_id.strip(),
        id=body.id.strip(),
        name=body.name.strip(),
        sender_id=body.sender_id.strip(),
        sender_type=body.sender_type.strip(),
        source_guid=body.source_guid.strip(),
        system=body.system,
        text=body.text.strip(),
        user_id=body.user_id.strip(),
    )
    db.add(message)
    db.commit()
