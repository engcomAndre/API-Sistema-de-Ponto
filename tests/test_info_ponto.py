import pytest

from tests.mockData import col1, col2
from api.models.PontoModel import Ponto


@pytest.fixture()
def web():
    from api.api import create_app
    app = create_app('testing')
    yield app


def test_compute_hours():
    ponto = Ponto(colaborador_id='12345678')
    ponto.criar_registro_ES()
    ponto.registrar_entrada_in('00:00:00')
    ponto.registrar_saida_in('10:00:00')

    pontos = [ponto.dict()]
    # TODO continuar e computar as horas it s easy

    res = Ponto.calcular_horas_mes(pontos)
    value = None
    ponto.remover()
    assert res, value
