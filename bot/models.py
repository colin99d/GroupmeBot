"""Models"""
__docformat__ = "numpy"

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()

BaseModel: DeclarativeMeta = db.Model


class Post(BaseModel):
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    avatar_url = db.Column(db.String(120))
    created_at = db.Column(db.String(350))
    group_id = db.Column(db.String(350))
    id = db.Column(db.String(350))
    name = db.Column(db.String(350))
    sender_id = db.Column(db.String(350))
    sender_type = db.Column(db.String(350))
    source_guid = db.Column(db.String(350))
    system = db.Column(db.Boolean)
    text = db.Column(db.String(10000))
    user_id = db.Column(db.String(350))

    def __repr__(self):
        return f"{self.text}"
