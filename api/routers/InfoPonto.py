from fastapi import APIRouter
from typing import List, Dict, Optional

from utils.responser_utils import gen_mensagem

from api.models.PontoModel import Ponto

router = APIRouter()


@router.get("/horas")
async def consultar_horas(colaborador_id: str, mes: str) -> Dict[str, str or Optional[List[Dict[str, str]]]]:
    try:
        pontos = Ponto.find(colaborador_id=colaborador_id, mes=mes)
        if not pontos:
            return {"mensagem": "Não existem pontos para o colaborador informado."}

        t_mes, output = Ponto.calcular_horas_mes(pontos)
        return gen_mensagem("Pontos computados", output)

    except:
        # TODO EXCEPT
        return gen_mensagem("Erro ao buscar informações de ponto.")
