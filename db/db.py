from pymongo import MongoClient
from pydantic import BaseModel


class Db:
    connect_db = MongoClient('mongodb://localhost:27017')
    db = connect_db.Desafio_Ponto

    @staticmethod
    def get_doc(document: str):
        return Db.db[document]

    @staticmethod
    def find(document: str, instance: BaseModel):
        return Db.get_doc(document).find(instance.dict())
        # # Todo find in document
        # pass

    @staticmethod
    def save(document: str, instance: BaseModel):
        return Db.get_doc(document).insert_one(instance.dict())
        # Todo save in document
        pass

    @staticmethod
    def update(document: str, instance: BaseModel, new_instance: BaseModel):
        return Db.get_doc(document).update_one(instance.dict(), new_instance.dict())
        # # Todo udpate in document
        # pass

    def delete(document: str, instance: BaseModel):
        return Db.get_doc(document).delete_one(instance.dict())
        # # Todo delete in document
        # pass
