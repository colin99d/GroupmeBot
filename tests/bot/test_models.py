from bot import models, utils, schemas
from tests import helpers as thelps


def test_post_str(db):
    data = thelps.get_post("Hello")
    schema = schemas.Message(**data)
    utils.add_post(db, schema)
    query = db.query(models.Post).all()
    assert str(query[-1]) == "@sportsbot Hello"
    assert len(query) == 1
