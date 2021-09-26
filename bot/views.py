from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

bot_name = ["SportsBot", "TestBot"]

def send_message(message):
    url = "https://api.groupme.com/v3/bots/post"
    bot_id = "5e6fccada121999d1dd6759d7a"
    group_id = "69502628"
    return requests.post(url=f"{url}?bot_id={bot_id}&text={message}")

@csrf_exempt
def handler(request):
    if request.method == "POST":
        send_message(request.body.decode('utf-8')["name"])
        if request.body.decode('utf-8')["name"] not in bot_name:
            send_message("Passed")
            return HttpResponse(status=200)
    else:
        http_resp = f"<p>The page is working.</p>"
        return HttpResponse(http_resp)
