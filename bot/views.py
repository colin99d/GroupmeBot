"""Bot views"""
__docformat__ = "numpy"

from . import utils
from .bible import text_to_verse
from . import data
from .ESPN import get_standings, win_chance


def handler(body):
    name: str = body.get("name").strip()
    text: str = body.get("text").strip().lower()
    user_id: str = body.get("user_id").strip()
    group_id: str = body.get("group_id").strip()

    if name != "SportsBot":
        if "retard" in text:
            utils.send_message("R-word hurts!!!", group_id)
            utils.remove_user(group_id, user_id)
            return

        message_dict = {
            "help": "Options:" + "".join([f"\n-{x}" for x in data.options]),
            ":": text_to_verse,
            "johnny": "Johnny its been years, reproduce already",
            "fantasy": "Stop the steal! The commish allows collusion!!!",
            "scores": get_standings,
            "voyager": utils.evan_voyager,
            "winner": win_chance,
            "insult": utils.random_insult,
            "card": utils.generate_card,
        }

        if "@sportsbot" in text:
            for key in message_dict.keys():
                if key in text:
                    val = message_dict[key]
                    if isinstance(val, str):
                        utils.send_message(val, group_id)
                    if val(text, group_id) is not None:
                        utils.send_message(val(text, group_id), group_id)
                    return
