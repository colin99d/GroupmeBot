"""app"""
__docformat__ = "numpy"

from flask import Flask, request, Response, render_template

from bot.views import handler
from bot import data

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        body = request.get_json(force=True)
        handler(body)
        return Response(status=201)
    print("Get")
    return render_template("home.html", result=data.options)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
