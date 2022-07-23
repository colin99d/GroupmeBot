import os
from typing import Any
from typing import List

from pydantic import BaseModel
from pydantic import BaseSettings


def create_path(*path: str) -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    in_between = os.path.dirname(base_path)
    default_path = os.path.join(in_between, *path)
    return default_path


class Message(BaseModel):
    attachments: List[Any]
    avatar_url: str
    created_at: int
    group_id: str
    id: str
    name: str
    sender_id: str
    sender_type: str
    source_guid: str
    system: bool
    text: str
    user_id: str


class Settings(BaseSettings):
    BIBLE_API_KEY: str
    ESPN_leagueID: str
    ESPN_SWID: str
    ESPN_S2: str
    GROUPME_TOKEN: str
    MAIN_GROUP_ID: str
    MAIN_GROUP_BOT: str
    TEST_GROUP_ID: str
    TEST_GROUP_BOT: str
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str


settings = Settings(_env_file=create_path(".env"))
