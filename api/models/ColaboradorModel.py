from pydantic import BaseModel, Schema, Required
from typing import List, Dict

from db.db import Db


class Colaborador(BaseModel):
    nome: str = Schema(Required, title="Nome do colaborador", min_length=5, max_length=120)
    endereco: str = Schema(None, title="Endereço do colaborador", min_length=5, max_length=120)
    cpf: str = Schema(Required, title="Cadastro Pessoa Fisica(CPF) da Colaborador.", regex="\\d{11}")

    def save(self) -> Dict:
        try:
            return self.dict() if Db.save("colaborador", self) else {}
        except:
            # TODO EXCEPT
            return {}

    def remove(self) -> bool:
        try:
            return True if Db.delete("colaborador", self) else None
        except:
            # TODO EXCEPT
            return False

    @classmethod
    def find(cls, colaborador_id: str = None, cpf: str = None) -> List[Dict[str,str]]:
        try:
            where = {}
            where.update({"_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})
            where.update({"cpf": f"{cpf.replace(' ', '')}"} if cpf else {})

            colaboradores = Db.find("colaborador", where)

            return colaboradores if colaboradores else None
        except:
            # TODO EXCEPT
            return []
