from fastapi import FastAPI
from config import config


def create_app(environment: str) -> FastAPI:
    app = FastAPI(__name__
                  , title="Desafio Ponto",
                  description="Api de um sistema de Ponto de uma empresa.",
                  version="1.0.0")
    from api.routers import load_routes
    from db.db import Db

    Db.db = config[environment].db
    app = load_routes(app)

    return app

