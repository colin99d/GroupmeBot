import pytest
from bot.database import Base
from bot.database import engine
from bot.database import get_db
from fastapi.testclient import TestClient
from main import app  # noqa: E402
from sqlalchemy.orm import Session


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
