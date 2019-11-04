from fastapi import APIRouter, Query
from typing import Dict

from api.models.ColaboradorModel import Colaborador

from utils.responser_utils import gen_mensagem

router = APIRouter()


@router.get("/")
async def consultar(
        colaborador_id: str = Query(None, title='Identificador', description="Identificador unico do colaborador"),
        cpf: str = Query(None, title='CPF', description="Campo CPF do colaborador")
) -> Dict[str, str]:
    try:
        colaboradores = Colaborador.find(colaborador_id=colaborador_id, cpf=cpf)
        if colaboradores:
            return gen_mensagem("Colaborador(es) encontrado(s).", colaboradores)
        return gen_mensagem("Colaborador(es) não encontrado(s) para os parametros informados.")
    except:
        # TODO EXCEPT
        return gen_mensagem("Problemas ao buscar colaboradores.")


@router.post("/")
async def criar(colaborador: Colaborador) -> Dict[str, str]:
    try:
        if Colaborador.find(cpf=colaborador.cpf):
            return gen_mensagem("Já existe colaborador cadastrado com o CPF informado")
        colaborador_salvo = colaborador.save()
        if colaborador_salvo:
            return gen_mensagem("Colaborador criado com sucesso", colaborador_salvo)
        return gen_mensagem("Problemas ao cadastrar colaborador")
    except:
        # TODO EXCEPT
        return gen_mensagem("Problemas ao criar colaboradores.")


@router.delete("/")
async def remover(
        colaborador_id: str = Query(None, title='Identificador', description="Identificador unico do colaborador"),
        cpf: str = Query(None, title='CPF', description="Campo CPF do colaborador")
) -> Dict[str, str]:
    try:
        if colaborador_id is None and cpf is None:
            return gen_mensagem("Ao menos um entre CPF e Id deve ser informado")

        colaborador_remover = Colaborador.find(colaborador_id, cpf)
        if not colaborador_remover:
            return gen_mensagem("Colaborador não encontrado para os parametros informados.")

        colaborador_remover = Colaborador(**colaborador_remover[0])
        if colaborador_remover.remover():
            return gen_mensagem("Colaborador removido com sucesso.")
        return gen_mensagem("Problemas ao exluir colaborador.")
    except:
        # TODO EXCEPT
        return gen_mensagem("Problemas ao remover colaboradores.")
