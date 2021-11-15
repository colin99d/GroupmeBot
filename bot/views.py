"""Bot views"""
__docformat__ = "numpy"

from . import data, bible, ESPN, utils, groupme


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
            "help": "Options:" + "".join([f"\n-{x}" for x in data.options]),
            ":": bible.text_to_verse,
            "johnny": "Johnny its been years, reproduce already",
            "fantasy": "Stop the steal! The commish allows collusion!!!",
            "scores": ESPN.get_standings,
            "voyager": utils.evan_voyager,
            "winner": ESPN.win_chance,
            "insult": utils.random_insult,
            "card": utils.generate_card,
            "nathan": utils.nathan,
        }

        if "@sportsbot" in text:
            for key in message_dict.keys():
                if key in text:
                    val = message_dict[key]
                    if isinstance(val, str):
                        groupme.send_message(val, group_id)
                    if val(text, group_id) is not None:
                        groupme.send_message(val(text, group_id), group_id)
                    return
