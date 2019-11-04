from pymongo import MongoClient
from pydantic import BaseModel
from uuid import uuid1
from typing import List, Dict


class Db:
    db: MongoClient

    @staticmethod
    def find(document: str, where: Dict, sort_by: str = None) -> List[Dict[str, str]]:
        if sort_by:
            return list(Db.db[document].find(where).sort(sort_by))
        return list(Db.db[document].find(where))

    @staticmethod
    def save(document: str, instance: BaseModel) -> Dict[str, str]:
        entity = {"_id": str(uuid1()), **instance.dict()}
        return entity if Db.db[document].insert_one(entity) else None

    @staticmethod
    def update(document: str, where: dict, new_instance: BaseModel) -> bool:
        return Db.db[document].update_one(where, {"$set": {**new_instance.dict()}})

    @staticmethod
    def delete(document: str, instance: BaseModel) -> bool:
        return Db.db[document].delete_one(instance.dict())
