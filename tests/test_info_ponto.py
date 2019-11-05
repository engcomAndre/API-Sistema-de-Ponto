import pytest

from api.routers.Ponto import colaborador_db
from tests.mockData import col1, col2
from api.models.PontoModel import Ponto
from api.models.ColaboradorModel import Colaborador
from utils.time_utils import date_format
import pendulum


@pytest.fixture()
def web():
    from api.api import create_app
    app = create_app('testing')
    yield app


def test_compute_hours():
    ponto = Ponto(colaborador_id=col1.colabaorador_id)
    ponto.registros_ES = [{'entrada': '00:00:00', 'saida': '10:00:00'}]

    #TODO continuar e computar as horas it s easy

    ponto.criar_registro_ES()
    ponto.registrar_entrada_in("10:00:00")
    ponto.registrar_saida_in("11:00:00")

    res = ponto.calcular_horas_mes()
    value = None
    ponto.remover()
    assert res, value
