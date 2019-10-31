import mongomock
import pytest


@pytest.fixture()
def db():
    mongo = mongomock.MongoClient().db.collection
    mongo.insert_one()


def test_save():
    mongo = mongomock.MongoClient().db.collection
    mongo.insert_one({'id': 123})
    result = mongo.find_one({'id': 123})
    assert result, True
