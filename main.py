"""app"""
__docformat__ = "numpy"

import os

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

from bot.models import db, User
from auth.views import auth
from bot.views import bot

load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(bot)

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


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
