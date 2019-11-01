from pymongo import MongoClient
from pydantic import BaseModel


class Db:
    db: str

    @staticmethod
    def init_db(mongo_url):
        Db.connect_db = MongoClient(mongo_url)
        Db.db = Db.connect_db.DesafioPonto

    @staticmethod
    def get_doc(document: str):
        return Db.db[document]

    @staticmethod
    def find(document: str, instance: BaseModel):
        return Db.get_doc(document).find(instance.dict())


    @staticmethod
    def save(document: str, instance: BaseModel):
        return Db.get_doc(document).insert_one(instance.dict())


    @staticmethod
    def update(document: str, instance: BaseModel, new_instance: BaseModel):
        return Db.get_doc(document).update_one(instance.dict(), new_instance.dict())

    def delete(document: str, instance: BaseModel):
        return Db.get_doc(document).delete_one(instance.dict())
