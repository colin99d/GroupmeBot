from . import bible
from . import ESPN
from . import groupme
from . import market
from . import schemas
from . import utils

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


def handler(body: schemas.Message):
    name: str = body.name.strip()
    text: str = body.text.strip().lower()
    user_id: str = body.user_id.strip()
    group_id: str = body.group_id.strip()

    if name != "SportsBot":
        if "retard" in text:
            groupme.send_message("R-word hurts!!!", group_id)
            groupme.remove_user(group_id, user_id)
            return

        if "@sportsbot" in text:
            for key, val in message_dict.items():
                if key in text:
                    if isinstance(val, str):
                        groupme.send_message(val, group_id)
                    elif val(text, group_id) is not None:
                        groupme.send_message(val(text, group_id), group_id)
                    return
            groupme.send_message(
                "Invalid command. Call 'help' for a list of commands", group_id
            )
            return
