from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import json

bot_names = ["SportsBot", "TestBot"]

def send_message(message):
    url = "https://api.groupme.com/v3/bots/post"
    bot_id = "5e6fccada121999d1dd6759d7a"
    group_id = "69502628"
    return requests.post(url=f"{url}?bot_id={bot_id}&text={message}")

@csrf_exempt
def handler(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        name = body.get("name").strip()
        text = body.get("text").strip()

        if name not in bot_names and ("@SportsBot" in text or "@TestBot" in text):
            if "help" in text.lower():
                send_message("Options:\n-Johnny\n-Fantasy")
            elif "johnny" in text.lower():
                send_message("Johnny its been years, reproduce already")
            elif "fantasy" in text.lower():
                send_message("Stop the steal! The commish allows collusion!!!")
            return HttpResponse(status=200)
    else:
        http_resp = f"<p>The page is working.</p>"
        return HttpResponse(http_resp)
