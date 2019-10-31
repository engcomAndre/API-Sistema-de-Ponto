from fastapi import APIRouter, Query
import pendulum

from pymongo import MongoClient
from utils.responser_utils import gen_mensagem
from models.ColaboradorModel import Colaborador
from models.PontoModel import Ponto

router = APIRouter()

client = MongoClient('mongodb://localhost:27017')
db = client.Desafio_Ponto
ponto_db = db["ponto"]
colaborador_db = db["colaborador"]

hour_format = "HH:mm:ss"
date_format = "DD/MM/YYYY"


@router.get('/')
def consultar(ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto"),
              data: str = Query(None, title="Data do ponto",
                                description="Data de registro do ponto ponto formato YYYYMMDD."),
              colaborador_id: str = Query(None, title="Identificador colaborador",
                                          description="Identificador unico do colaborador."),
              mes: str = Query(None, title="Mes do ano.",
                               description="Mes em formato numérico(Janeiro - 01,Fevereiro - 02...")
              ):
    pontos = Ponto.find(ponto_id,  colaborador_id,data, mes)
    if pontos:
        return gen_mensagem("Pontos encotrados", pontos)
    return gen_mensagem("Pontos não encontrados para os parametros informados.")


@router.post('/')
def criar(ponto: Ponto):
    mes = str(pendulum.now().month)
    colaborador = Colaborador.find(ponto.colaborador_id)
    if not colaborador:
        return gen_mensagem("Não existe colaborador para os parametros informados.")
    ultimo_ponto = Ponto.find(colaborador_id=ponto.colaborador_id, mes=mes)
    ultimo_ponto = ultimo_ponto.pop() if ultimo_ponto else []
    if not ultimo_ponto:
        if Ponto.abrir_registro_ES(ponto.colaborador_id):
            return gen_mensagem("Ponto registrado com sucesso.")

    dif_dias = pendulum.period(pendulum.from_format(ultimo_ponto["data"], date_format), pendulum.now()).in_days()

    if dif_dias > 0:
        if dif_dias == 1 and Ponto.registrar_virada(ultimo_ponto,
                                                    ponto.colaborador_id):  # Registro de virada onde houve virada de dia
            return gen_mensagem("Ponto registrado com sucesso.")
        if Ponto.registrar_entrada(ultimo_ponto):
            return gen_mensagem("Ponto registrado com sucesso.")

    elif dif_dias == 0:
        if Ponto.registrar_entrada(ultimo_ponto):
            return gen_mensagem("Ponto registrado com sucesso.")
        elif Ponto.registrar_saida(ultimo_ponto):
            return gen_mensagem("Ponto registrado com sucesso.")
    return gen_mensagem("Problema ao registrar o ponto.")


@router.delete("/{ponto_id}")
def remover(ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto")):
    if not Ponto.find(ponto_id):
        return gen_mensagem("Não exitem pontos para os parametros informados.")

    if Ponto.remover(ponto_id):
        return gen_mensagem("Ponto removido com sucesso")
    return gen_mensagem("Problemas ao excluir ponto")
