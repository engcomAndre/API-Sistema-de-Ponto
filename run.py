from fastapi import FastAPI

from routers import load_routes


def create_app(config_name: str):
    app = FastAPI(__name__
                  , title="Desafio Ponto",
                  description="Api de um sistema de Ponto de uma empresa.",
                  version="1.0.0")
    app = load_routes(app)
    return app
