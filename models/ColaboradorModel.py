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

    def save(self):
        return self.to_dict() if Db.save("colaborador", self) else None

    def remove(self):
        return True if Db.delete("colaborador", self) else None

    @classmethod
    def find(cls, colaborador_id: str = None, cpf: str = None):
        where = {}
        where.update({"_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})
        where.update({"cpf": f"{cpf.replace(' ', '')}"} if cpf else {})

        colaboradores = Db.find("colaborador",where)

        return colaboradores if colaboradores else None

    def to_dict(self):
        return {"Nome": self.nome, "Endereco": self.endereco, "CPF": self.cpf}
