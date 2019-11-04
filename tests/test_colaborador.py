import pytest
from tests.mockData import col1, col2
from api.models.ColaboradorModel import Colaborador

@pytest.fixture()
def web():
    from api.api import create_app
    app = create_app('testing')
    yield app


def test_instance_erro_empty():
    with pytest.raises(Exception):
        assert Colaborador()


def test_instance_erro_values():
    with pytest.raises(Exception):
        assert Colaborador(nome="Andr", cpf='12131213')


def test_save_find(web):
    col1.save()
    col_recuperado = Colaborador.find(cpf=col1.cpf)
    col_recuperado = Colaborador(**col_recuperado[0])
    assert col1, col_recuperado


def test_remove(web):
    col1.remover()
    col_recuperado = Colaborador.find(cpf=col1.cpf)
    assert str(None), str(col_recuperado)
