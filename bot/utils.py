"""Bot utils"""
__docformat__ = "numpy"
import json

import html
from random import randint

import requests
from sqlalchemy import func, desc

from . import groupme, models
from bot.models import db, Post


def get_random(lst):
    amount = len(lst)
    rnd = randint(0, amount - 1)
    return lst[rnd]


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
    with open("bot/data/players.json") as json_file:
        players = json.load(json_file)
    selection = get_random(list(players))
    p = players[selection]
    strengths: str = "".join([x + "\n" for x in p["Strengths"]])
    weaknesses: str = "".join([x + "\n" for x in p["Weaknesses"]])
    selection += (
        f"\n{p['Description']}\n\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"
    )
    groupme.send_image(p["image"], group_id, selection)


def handle_stats(_, group_id):
    query = (
        models.db.session.query(
            models.Post.name, func.count(models.Post.name).label("name_count")
        )
        .group_by(models.Post.name)
        .filter_by(group_id=group_id)
        .order_by(desc("name_count"))
    )
    string = "Messages by user:"
    for item in query.all():
        string += f"\n{item[0]} {item[1]}"
    return string


def add_post(body):
    avatar_url = str(body.get("avatar_url")).strip()
    created_at = str(body.get("created_at")).strip()
    group_id = str(body.get("group_id")).strip()
    id = str(body.get("id")).strip()
    name = str(body.get("name")).strip()
    sender_id = str(body.get("sender_id")).strip()
    sender_type = str(body.get("sender_type")).strip()
    source_guid = str(body.get("source_guid")).strip()
    system = body.get("system")
    text = str(body.get("text")).strip()
    user_id = str(body.get("user_id")).strip()
    message = Post(
        avatar_url=avatar_url,
        created_at=created_at,
        group_id=group_id,
        id=id,
        name=name,
        sender_id=sender_id,
        sender_type=sender_type,
        source_guid=source_guid,
        system=system,
        text=text,
        user_id=user_id,
    )
    db.session.add(message)
    db.session.commit()
