import pytest
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


def test_instance_erro_empty():
    with pytest.raises(Exception):
        assert Ponto()


def test_instance_erro_values():
    with pytest.raises(Exception):
        assert Ponto(colaborador_id=None)


def test_save_find(web):
    col1.save()
    col_test = Colaborador.find(cpf=col1.cpf)
    colaborador_id = col_test[0]['_id']
    col1.remover()

    ponto_salvo = Ponto(colaborador_id=colaborador_id)
    ponto_salvo.criar_registro_ES()

    ponto_rec = Ponto.find(colaborador_id=ponto_salvo.colaborador_id, data=pendulum.now().format(date_format))
    ponto_salvo.remover()
    assert ponto_rec, ponto_salvo


def test_remove(web):
    col1.save()
    col_test = Colaborador.find(cpf=col1.cpf)
    colaborador_id = col_test[0]['_id']
    col1.remover()

    ponto_salvo = Ponto(colaborador_id=colaborador_id)
    ponto_salvo.criar_registro_ES()

    ponto_rec = Ponto.find(colaborador_id=ponto_salvo.colaborador_id, data=pendulum.now().format(date_format))
    assert ponto_rec, ponto_salvo
    ponto_salvo.remover()
    ponto_rec = Ponto.find(colaborador_id=ponto_salvo.colaborador_id, data=pendulum.now().format(date_format))
    assert str(ponto_rec), str(None)
