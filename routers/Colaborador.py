from fastapi import APIRouter, Query

from models.ColaboradorModel import Colaborador

from utils.responser_utils import gen_mensagem

router = APIRouter()


@router.get("/")
async def consultar(
        colaborador_id: str = Query(None, title='Identificador', description="Identificador unico do colaborador"),
        cpf: str = Query(None, title='CPF', description="Campo CPF do colaborador")
):
    colaboradores = Colaborador.find(colaborador_id=colaborador_id, cpf=cpf)
    if colaboradores:
        return gen_mensagem("Colaborador(es) encontrado(s).", colaboradores)
    return gen_mensagem("Colaborador(es) não encontrado(s) para os parametros informados.")


@router.post("/")
async def criar(colaborador: Colaborador):
    if Colaborador.find(cpf=colaborador.cpf):
        return gen_mensagem("Já existe colaborador cadastrado com o CPF informado")
    colaborador_salvo = colaborador.save()
    if colaborador_salvo:
        return gen_mensagem("Colaborador criado com sucesso", colaborador_salvo)
    return gen_mensagem("Problemas ao cadastrar colaborador")


@router.delete("/")
async def remover(
        colaborador_id: str = Query(None, title='Identificador', description="Identificador unico do colaborador"),
        cpf: str = Query(None, title='CPF', description="Campo CPF do colaborador")
):
    if colaborador_id is None and cpf is None:
        return gen_mensagem("Ao menos um entre CPF e Id deve ser informado")

    colaborador_remover = Colaborador.find(colaborador_id, cpf)
    if not colaborador_remover:
        return gen_mensagem("Colaborador não encontrado para os parametros informados.")

    if Colaborador.remove(colaborador_remover[0]):
        return gen_mensagem("Colaborador removido com sucesso.")
    return gen_mensagem("Problemas ao exluir colaborador.")

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
