"""Models"""
__docformat__ = "numpy"

from typing import Any
import sqlalchemy as sa
from . import database

Base: Any = database.Base

class Post(Base):
    __tablename__ = "post"

    pk = sa.Column(sa.Integer, primary_key=True, nullable=False)
    avatar_url = sa.Column(sa.String(120))
    created_at = sa.Column(sa.String(350))
    group_id = sa.Column(sa.String(350))
    id = sa.Column(sa.String(350))
    name = sa.Column(sa.String(350))
    sender_id = sa.Column(sa.String(350))
    sender_type = sa.Column(sa.String(350))
    source_guid = sa.Column(sa.String(350))
    system = sa.Column(sa.Boolean)
    text = sa.Column(sa.String(10000))
    user_id = sa.Column(sa.String(350))

    def __repr__(self):
        return f"{self.text}"


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(100), unique=True)
    password = sa.Column(sa.String(100))
    name = sa.Column(sa.String(1000))
