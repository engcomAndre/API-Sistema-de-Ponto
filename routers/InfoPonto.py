from fastapi import APIRouter
from pymongo import MongoClient
import re
import pendulum

router = APIRouter()

client = MongoClient('mongodb://localhost:27017')
db = client.Desafio_Ponto
colaborador_db = db["colaborador"]
ponto_db = db["ponto"]


@router.get("/horas")
def consultar_horas(colaborador_id: str, mes: int):
    where = {"_id": colaborador_id}

    if not colaborador_db.find(where):
        return {"mensagem": "Colaborador(es) não encontrado(s) para os parametros informados."}

    where = {"colaborador_id": colaborador_id}
    rex = re.compile(f"\d\d\d\d{mes}\d\d")
    where.update({"data": rex})
    pontos_mes = list(ponto_db.find(where).sort("data"))

    output = []
    date_format = "%H:%M:%S"
    t_duracao_mes = 0
    for ponto in pontos_mes:
        t_duracao_dia = 0
        for io in ponto['registros_ES']:  # calcula a duração do dia
            h_saida = pendulum.parse(io["saida"])
            h_entrada = pendulum.parse(io["entrada"])
            period = pendulum.period(h_entrada, h_saida).in_seconds()
            t_duracao_dia = t_duracao_dia + period
            t_duracao_mes = t_duracao_mes + period
        data = pendulum.parse(ponto["data"])
        output.append({"_id" : ponto["_id"],"data": data.format("DD/MM/YYYY"), "horas trabalhadas no dia": format_date(t_duracao_dia)})
    return {"mensagem": "Pontos Horas computados ", "pontos": output, "Total de horas trabalhadas no mês": format_date(t_duracao_mes)}


def format_date(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    str = '{:}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
    return (str)