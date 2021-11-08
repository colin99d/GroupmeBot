"""app"""
__docformat__ = "numpy"

from flask import Flask, request, Response

from bot.views import handler

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        body = request.get_json(force=True)
        handler(body)
        return Response(status=201)
    return "<h1>Gamestonk GroupmeBot URL</h1>"


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
