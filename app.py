"""app"""
__docformat__ = "numpy"
import json

from flask import Flask, request, Response, render_template

from bot.views import handler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        body = request.get_json(force=True)
        handler(body)
        return Response(status=201)
    with open("bot/data/options.json") as json_file:
        options = json.load(json_file)
    return render_template("home.html", result=options)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
