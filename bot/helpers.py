from typing import Optional

from sqlalchemy.orm import Session

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
    "winner": ESPN.win_chance,
    "stock": market.chart_stock,
    "voyager": market.evan_voyager,
    "insult": utils.random_insult,
    "card": utils.generate_card,
    "stats": utils.handle_stats,
}


def handler(body: schemas.Message, db: Session):
    name: str = body.name.strip()
    text: str = body.text.strip().lower()
    user_id: str = body.user_id.strip()
    group_id: str = body.group_id.strip()
    message: Optional[str] = None

    if name != "SportsBot":
        if "retard" in text:
            groupme.send_message("R-word hurts!!!", group_id)
            groupme.remove_user(group_id, user_id)
            return

        if "@sportsbot" in text:
            for key, val in message_dict.items():
                if key in text:
                    if isinstance(val, str):
                        message = val
                    elif callable(val):
                        message = val(text=text, group_id=group_id, db=db)
                    else:
                        message = "Invalid command. Call 'help' for a list of commands"
                    break
            if message:
                groupme.send_message(message, group_id)
