from routers import Colaborador, InfoPonto, Ponto


def load_routes(app):
    app.include_router(Ponto.router, prefix="/ponto", tags=["Ponto"])
    app.include_router(Colaborador.router, prefix="/colaborador", tags=["Colaborador"])
    app.include_router(InfoPonto.router, prefix="/info", tags=["Ponto_Info"])
    return app
