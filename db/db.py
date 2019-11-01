from pymongo import MongoClient
from pydantic import BaseModel
from uuid import uuid1


class Db:
    db: MongoClient

    @staticmethod
    def find(document: str, instance: BaseModel):
        return list(Db.db[document].find(instance))

    @staticmethod
    def save(document: str, instance: BaseModel):
        return Db.db[document].insert_one({"_id": str(uuid1()), **instance.dict()})

    @staticmethod
    def update(document: str, instance: BaseModel, new_instance: BaseModel):
        return Db.db[document].update_one(instance.dict(), new_instance.dict())

    @staticmethod
    def delete(document: str, instance: BaseModel):
        return Db.db[document].delete_one(instance)
