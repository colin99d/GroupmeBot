"""app"""
__docformat__ = "numpy"
import json
import os

from flask import Flask, request, Response, render_template
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from dotenv import load_dotenv

from bot.views import handler
from bot.models import db, Post, User
from auth.views import auth


load_dotenv()


app = Flask(__name__)
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        body = request.get_json(force=True)
        handler(body)
        add_post(body)
        return Response(status=201)
    with open("bot/data/options.json") as json_file:
        options = json.load(json_file)
    return render_template("home.html", result=options)


@login_required
@app.route("/messages", methods=["GET"])
def messages():
    if request.method == "GET":
        return render_template("messages.html", users=Post.query.all())


if __name__ == "__main__":
    app.run(threaded=True, port=5000)


def add_post(body):
    avatar_url = str(body.get("avatar_url")).strip()
    created_at = str(body.get("created_at")).strip()
    group_id = str(body.get("group_id")).strip()
    id = str(body.get("id")).strip()
    name = str(body.get("name")).strip()
    sender_id = str(body.get("sender_id")).strip()
    sender_type = str(body.get("sender_type")).strip()
    source_guid = str(body.get("source_guid")).strip()
    system = body.get("system")
    text = str(body.get("text")).strip()
    user_id = str(body.get("user_id")).strip()
    message = Post(
        avatar_url=avatar_url,
        created_at=created_at,
        group_id=group_id,
        id=id,
        name=name,
        sender_id=sender_id,
        sender_type=sender_type,
        source_guid=source_guid,
        system=system,
        text=text,
        user_id=user_id,
    )
    db.session.add(message)
    db.session.commit()
