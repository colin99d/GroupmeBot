from django.http import HttpResponse
from django.shortcuts import render
import requests


def send_message(message):
    url = "https://api.groupme.com/v3/bots/post"
    bot_id = "5e6fccada121999d1dd6759d7a"
    group_id = "69502628"
    return requests.post(url=f"{url}?bot_id={bot_id}&text={message}")


def handler(request):
    if request.method == "POST":
        response = send_message("Whats up? Crackers!")
        return HttpResponse(status=200)
    else:
        response = send_message("Whats up? Crackers!")
        http_resp = f"<p>The response was: {response}</p>"
        return HttpResponse(http_resp)
