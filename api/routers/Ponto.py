from fastapi import APIRouter, Query
import pendulum

from pymongo import MongoClient
from utils.responser_utils import gen_mensagem
from api.models.ColaboradorModel import Colaborador
from api.models.PontoModel import Ponto

router = APIRouter()

client = MongoClient('mongodb://localhost:27017')
db = client.Desafio_Ponto
ponto_db = db["ponto"]
colaborador_db = db["colaborador"]

hour_format = "HH:mm:ss"
date_format = "DD/MM/YYYY"


@router.get('/')
def consultar(
        ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto"),
        data: str = Query(None, title="Data do ponto",
                          description="Data de registro do ponto ponto formato YYYYMMDD."),
        colaborador_id: str = Query(None, title="Identificador colaborador",
                                    description="Identificador unico do colaborador."),
        mes: str = Query(None, title="Mes do ano.",
                         description="Mes em formato numérico(Janeiro - 01,Fevereiro - 02...")
):
    try:
        pontos = Ponto.find(ponto_id, colaborador_id, data, mes)
        if pontos:
            return gen_mensagem("Pontos encotrados", pontos)
        return gen_mensagem("Pontos não encontrados para os parametros informados.")
    except:
        #TODO EXCEPT
        return gen_mensagem("Erro ao excluir ponto")


@router.post('/')
def criar(
        colaborador_id: str = Query(..., title="ID colaborador", description="Identificador único do identificador.")):
    mes = str(pendulum.now().month)
    try:
        colaborador = Colaborador.find(colaborador_id=colaborador_id)
        if not colaborador:
            return gen_mensagem("Não existe colaborador para os parametros informados.")

        ultimo_ponto = Ponto.find(colaborador_id=colaborador_id, mes=mes)
        ultimo_ponto = ultimo_ponto.pop() if ultimo_ponto else {'colaborador_id': colaborador_id}

        ponto = Ponto(**ultimo_ponto)

        if ponto.e_entrada() and ponto.registrar_entrada_in():
            return gen_mensagem("Ponto registrado com sucesso.", ponto.dict())
        elif ponto.e_virada() and ponto.registrar_virada_in():
            return gen_mensagem("Ponto registrado com sucesso.", ponto.dict())
        elif ponto.registrar_saida_in():
            return gen_mensagem("Ponto registrado com sucesso.", ponto.dict())
        return gen_mensagem("Problema ao registrar o ponto.")

    except:
        #TODO EXCEPT
        return gen_mensagem("Erro ao excluir ponto")


@router.delete("/{ponto_id}")
def remover(ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto")):
    try:
        ponto = Ponto.find(ponto_id)
        if not ponto:
            return gen_mensagem("Não exitem pontos para os parametros informados.")
        ponto = Ponto(**ponto[0])
        if ponto.remover():
            return gen_mensagem("Ponto removido com sucesso")
        return gen_mensagem("Problemas ao excluir ponto")
    except:
        #TODO EXCEPT
        return gen_mensagem("Erro ao excluir ponto")
