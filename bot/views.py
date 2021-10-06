"""Bot views"""
__docformat__ = "numpy"

import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .ESPN import get_standings, win_chance
from .utils import (
    evan_voyager,
    remove_user,
    send_message,
    random_insult,
    get_random,
    send_image,
)
from .data import players

options = ["Johnny", "Fantasy", "Scores", "Voyager", "Winner", "Insult", "Card"]


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
                remove_user(group_id, user_id)

            if "@sportsbot" in text:
                if "help" in text:
                    message = "Options:"
                    for opt in options:
                        message += f"\n-{opt}"
                elif "johnny" in text:
                    message = "Johnny its been years, reproduce already"
                elif "fantasy" in text:
                    message = "Stop the steal! The commish allows collusion!!!"
                elif "scores" in text:
                    message = get_standings()
                elif "voyager" in text:
                    message = evan_voyager()
                elif "winner" in text:
                    message = win_chance()
                elif "insult" in text:
                    message = random_insult(group_id)
                elif "card" in text:
                    selection = get_random([x for x in players])
                    p = players[selection]
                    send_image(p["image"], group_id, selection)
                    strengths: str = ""
                    weaknesses: str = ""
                    for strength in p["Strengths"]:
                        strengths += strength + "\n"
                    for weakness in p["Weaknesses"]:
                        weaknesses += weakness + "\n"
                    message = f"{p['Description']}\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}"
            if message:
                send_message(message, group_id)

        return HttpResponse(status=200)
    else:
        message = get_standings()
        http_resp = "<p>The website is running.</p>"
        return HttpResponse(http_resp)
