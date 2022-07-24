import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from bot.database import Base, engine, get_db
from main import app  # noqa: E402

# pylint:disable = W0621


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("api-key", "DUMMY"), ("Cookie", "DUMMY")],
        "filter_query_parameters": [("api_key", "DUMMY"), ("token", "DUMMY")],
    }


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    print(db_engine.url.database)
    connection = db_engine.connect()
    connection.begin()
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


# pylint: disable=W0621
@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    # Using testclient in a context manager triggers on_event
    c = TestClient(app)
    return c


def return_message(**kwargs):
    del kwargs
    return "A friendly message"


@pytest.fixture(scope="function")
def mock_actions(mocker):
    new_dict = {
        x: return_message
        for x in [
            "bible",
            "scores",
            "winner",
            "stock",
            "voyager",
            "insult",
            "card",
            "stats",
        ]
    }
    mocker.patch("bot.helpers.message_dict", new_dict)
