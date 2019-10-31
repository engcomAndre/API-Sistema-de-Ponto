import uvicorn
from fastapi import FastAPI

from routers import Colaborador, InfoPonto, Ponto

app = FastAPI(__name__
              , title="Desafio Ponto",
              description="Api de um sistema de Ponto de uma empresa.",
              version="1.0.0")

app.include_router(Ponto.router, prefix="/ponto", tags=["Ponto"])
app.include_router(Colaborador.router, prefix="/colaborador", tags=["Colaborador"])
app.include_router(InfoPonto.router, prefix="/info", tags=["Ponto_Info"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
