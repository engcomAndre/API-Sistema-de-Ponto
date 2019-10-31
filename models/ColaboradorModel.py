from pydantic import BaseModel, Schema, Required
#
# client = MongoClient('mongodb://localhost:27017')
# db = client.Desafio_Ponto
# colaborador_db = db["colaborador"]
from db.db import Db


class Colaborador(BaseModel):
    nome: str = Schema(Required, title="Nome do colaborador", min_length=5, max_length=120)
    endereco: str = Schema(None, title="Endereço do colaborador", min_length=5, max_length=120)
    cpf: str = Schema(Required, title="Cadastro Pessoa Fisica(CPF) da Colaborador.", regex="\d{11}")

    # def __init__(self, nome: str, cpf: str, endereco: str = None):
    #     self.nome = nome
    #     self.endereco = endereco
    #     self.cpf = cpf

    def save(self):
        return self.to_dict() if Db.save("colaborador", self) else None
        # return self.to_dict() if get_doc(self.document).insert_one({"_id": str(uuid1()), **self.to_dict()}) else None

    @classmethod
    def remove(cls, colaborador: dict):
        return True if Db.save("colaborador", colaborador) else None

        # return True if colaborador_db.delete_one(colaborador) else False

    @classmethod
    def find(cls, colaborador_id: str = None, cpf: str = None):
        where = {}
        where.update({"_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})
        where.update({"CPF": f"{cpf.replace(' ', '')}"} if cpf else {})

        colaborador_db = Db.get_doc("colaborador")

        colaboradores = list(colaborador_db.find(where))

        return colaboradores if colaboradores else None

    def to_dict(self):
        return {"Nome": self.nome, "Endereco": self.endereco, "CPF": self.cpf}
