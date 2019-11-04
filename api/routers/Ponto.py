from fastapi import APIRouter, Query
import pendulum
from typing import Dict

from utils.responser_utils import gen_mensagem
from api.models.ColaboradorModel import Colaborador
from api.models.PontoModel import Ponto

router = APIRouter()


@router.get('/')
def consultar(
        ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto"),
        data: str = Query(None, title="Data do ponto",
                          description="Data de registro do ponto ponto formato YYYYMMDD."),
        colaborador_id: str = Query(None, title="Identificador colaborador",
                                    description="Identificador unico do colaborador."),
        mes: str = Query(None, title="Mes do ano.",
                         description="Mes em formato numérico(Janeiro - 01,Fevereiro - 02...")
) -> Dict[str, str]:
    try:
        pontos = Ponto.find(ponto_id, colaborador_id, data, mes)
        if pontos:
            return gen_mensagem("Pontos encotrados", pontos)
        return gen_mensagem("Pontos não encontrados para os parametros informados.")
    except:
        # TODO EXCEPT
        return gen_mensagem("Erro ao excluir ponto")


@router.post('/criar')
def criar(colaborador_id: str, data: str, hora_entrada: str, hora_saida: str) -> Dict[str, str]:
    ponto = Ponto(colaborador_id=colaborador_id, data=data)
    try:
        ponto.registros_ES.append({"entrada": hora_entrada, "saida": hora_saida})
        if ponto.save():
            return gen_mensagem("Ponto criado com sucesso.", [ponto.dict()])
    except:
        # TODO EXCEPT
        return gen_mensagem("Erro ao criar ponto..")


@router.post('/registrar_ponto')
def registrar_ponto(
        colaborador_id: str = Query(..., title="ID colaborador",
                                    description="Identificador único do identificador.")) -> Dict[str, str]:
    mes = str(pendulum.now().month)
    try:
        colaborador = Colaborador.find(colaborador_id=colaborador_id)
        if not colaborador:
            return gen_mensagem("Não existe colaborador para os parametros informados.")

        ultimo_ponto = Ponto.find(colaborador_id=colaborador_id, mes=mes)
        ultimo_ponto = ultimo_ponto.pop() if ultimo_ponto else {'colaborador_id': colaborador_id}

        ponto = Ponto(**ultimo_ponto)

        if ponto.e_entrada() and ponto.registrar_entrada_in():
            return gen_mensagem("Ponto registrado com sucesso.", [ponto.dict()])
        elif ponto.e_virada() and ponto.registrar_virada_in():
            return gen_mensagem("Ponto registrado com sucesso.", [ponto.dict()])
        elif ponto.registrar_saida_in():
            return gen_mensagem("Ponto registrado com sucesso.", [ponto.dict()])
        return gen_mensagem("Problema ao registrar o ponto.")

    except:
        # TODO EXCEPT
        return gen_mensagem("Erro ao registrar ponto")


@router.delete("/{ponto_id}")
def remover(ponto_id: str = Query(None, title="Id ponto", description="Id unico de um ponto")) -> Dict[str, str]:
    try:
        ponto = Ponto.find(ponto_id)
        if not ponto:
            return gen_mensagem("Não exitem pontos para os parametros informados.")
        ponto = Ponto(**ponto[0])
        if ponto.remover():
            return gen_mensagem("Ponto removido com sucesso")
        return gen_mensagem("Problemas ao excluir ponto")
    except:
        # TODO EXCEPT
        return gen_mensagem("Erro ao excluir ponto")
