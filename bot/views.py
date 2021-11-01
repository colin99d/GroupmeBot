"""Bot views"""
__docformat__ = "numpy"

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import utils
from .bible import text_to_verse
from .data import players
from .ESPN import get_standings, win_chance


options = [
    "Johnny",
    "Fantasy",
    "Scores",
    "Voyager",
    "Winner",
    "Insult",
    "Card",
    "Book Chapter:Verse",
]


@csrf_exempt
def handler(request):
    if request.method == "POST":
        body: str = json.loads(request.body.decode("utf-8"))
        name: str = body.get("name").strip()
        text: str = body.get("text").strip().lower()
        user_id: str = body.get("user_id").strip()
        group_id: str = body.get("group_id").strip()
        message: str = ""

        if name != "SportsBot":
            if "retard" in text:
                message = "R-word hurts!!!"
                utils.remove_user(group_id, user_id)

            if "@sportsbot" in text:
                if "help" in text:
                    message = "Options:"
                    for opt in options:
                        message += f"\n-{opt}"
                elif ":" in text:
                    message = text_to_verse(text)
                elif "johnny" in text:
                    message = "Johnny its been years, reproduce already"
                elif "fantasy" in text:
                    message = "Stop the steal! The commish allows collusion!!!"
                elif "scores" in text:
                    message = get_standings()
                elif "voyager" in text:
                    message = utils.evan_voyager()
                elif "winner" in text:
                    message = win_chance()
                elif "insult" in text:
                    message = utils.random_insult(group_id)
                elif "harass" in text:
                    utils.direct_message(group_id, user_id)
                elif "card" in text:
                    selection = utils.get_random(list(players))
                    p = players[selection]
                    utils.send_image(p["image"], group_id, selection)
                    strengths: str = ""
                    weaknesses: str = ""
                    for strength in p["Strengths"]:
                        strengths += strength + "\n"
                    for weakness in p["Weaknesses"]:
                        weaknesses += weakness + "\n"
                    message = f"{p['Description']}\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"
            if message:
                utils.send_message(message, group_id)

        return HttpResponse(status=200)
    else:
        message = get_standings()
        http_resp = "<p>The website is running.</p>"
        return HttpResponse(http_resp)
