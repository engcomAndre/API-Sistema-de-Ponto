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
    ponto.data = '11/11/1111'
    ponto.registros_ES = [{'entrada': '08:00:00', 'saida': '12:00:00'}, {'entrada': '13:00:00', 'saida': '18:00:00'}]

    ponto2 = Ponto(colaborador_id='12345678')
    ponto2.data = '12/11/1111'
    ponto2.registros_ES = [{'entrada': '08:00:00', 'saida': '12:00:00'}, {'entrada': '13:00:00', 'saida': '18:00:00'}]

    pontos = [ponto.dict(), ponto2.dict()]
    res1, res2 = 64800, {'Total de tempo Trabalhado no mês': '18:00:00',
                         'Total de horas por dia': [{'Data': '11/11/1111', 'Horas Trabalhadas no dia': '9:00:00'},
                                                    {'Data': '12/11/1111', 'Horas Trabalhadas no dia': '9:00:00'}]}
    val1, val2 = Ponto.calcular_horas_mes(pontos)

    assert res1, val1
    assert res2, val2

