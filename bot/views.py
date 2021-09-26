from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import json

bot_names = ["SportsBot", "TestBot"]

def send_message(message, group_id):
    url = "https://api.groupme.com/v3/bots/post"
    if group_id == "69502628":
        bot_id = "5e6fccada121999d1dd6759d7a"
    elif group_id == "46166401":
        bot_id = "d1d19ce1822d3080e157027858"

    return requests.post(url=f"{url}?bot_id={bot_id}&text={message}")

"""
def fantasy_api():
    league_id = 1659909443
    year = 2021
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id) + "?seasonId=" + str(year)
    r = requests.get(url)
"""

@csrf_exempt
def handler(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        name = body.get("name").strip()
        text = body.get("text").strip()
        group_id = body.get("group_id").strip()
        if name not in bot_names and ():
            if "retard" in text.lower():
                send_message("R-word hurts!!!", group_id)
            if "@SportsBot" in text or "@TestBot" in text:
                if "help" in text.lower():
                    send_message("Options:\n-Johnny\n-Fantasy\n\nAnd NO saying the r-word!", group_id)
                elif "johnny" in text.lower():
                    send_message("Johnny its been years, reproduce already", group_id)
                elif "fantasy" in text.lower():
                    send_message("Stop the steal! The commish allows collusion!!!", group_id)
                return HttpResponse(status=200)
    else:
        http_resp = f"<p>The page is working.</p>"
        return HttpResponse(http_resp)
