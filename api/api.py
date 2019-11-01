from fastapi import FastAPI


def create_app():
    app = FastAPI(__name__
                  , title="Desafio Ponto",
                  description="Api de um sistema de Ponto de uma empresa.",
                  version="1.0.0")

    from routers import load_routes
    from pymongo import MongoClient
    from db.db import Db

    Db.db = MongoClient('mongodb://localhost:27017').DesafioPonto

    app = load_routes(app)

    return app
