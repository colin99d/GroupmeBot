import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .ESPN import get_standings, win_chance
from .utils import evan_voyager, remove_user, send_message

bot_names = ["SportsBot", "TestBot"]

options = ["Johnny", "Fantasy", "Scores", "Voyager", "Winner"]

@csrf_exempt
def handler(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        name = body.get("name").strip()
        text = body.get("text").strip().lower()
        user_id = body.get("user_id").strip()
        group_id = body.get("group_id").strip()
        
        if name not in bot_names:
            if "retard" in text:
                send_message("R-word hurts!!!", group_id)
                remove_user(group_id, user_id)
            if "@sportsbot" in text or "@testbot" in text:
                if "help" in text:
                    message = "Options:"
                    for opt in options:
                        message += f"\n-{opt}"
                    send_message(message, group_id)
                elif "johnny" in text:
                    send_message("Johnny its been years, reproduce already", group_id)
                elif "fantasy" in text:
                    send_message("Stop the steal! The commish allows collusion!!!", group_id)
                elif "scores" in text:
                    message = get_standings()
                    send_message(message, group_id)
                elif "voyager" in text:
                    message = evan_voyager()
                    send_message(message, group_id)
                elif "winner" in text:
                    message = win_chance()
                    send_message(message, group_id)

        return HttpResponse(status=200)
    else:
        message = get_standings()
        http_resp = f"<p>The website is running.</p>"
        return HttpResponse(http_resp)
