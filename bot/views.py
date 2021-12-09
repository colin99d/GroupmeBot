"""Bot views"""
__docformat__ = "numpy"
# from flask import Blueprint

from . import bible, ESPN, utils, groupme, market

# bot = Blueprint('bot', __name__)


def handler(body):
    name: str = body.get("name").strip()
    text: str = body.get("text").strip().lower()
    user_id: str = body.get("user_id").strip()
    group_id: str = body.get("group_id").strip()

    if name != "SportsBot":
        if "retard" in text:
            groupme.send_message("R-word hurts!!!", group_id)
            groupme.remove_user(group_id, user_id)
            return

        message_dict = {
            "help": "https://mygroupmetestbot.herokuapp.com/",
            "bible": bible.text_to_verse,
            "scores": ESPN.get_standings,
            "voyager": market.evan_voyager,
            "winner": ESPN.win_chance,
            "insult": utils.random_insult,
            "card": utils.generate_card,
            "stock": market.chart_stock,
            "stats": utils.handle_stats,
        }

        if "@sportsbot" in text:
            for key in message_dict.keys():
                if key in text:
                    val = message_dict[key]
                    if isinstance(val, str):
                        groupme.send_message(val, group_id)
                    elif val(text, group_id) is not None:
                        groupme.send_message(val(text, group_id), group_id)
                    return
            groupme.send_message(
                "Invalid command. Call 'help' for a list of commands", group_id
            )
            return
