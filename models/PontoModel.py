import re
from uuid import uuid1
from pydantic import BaseModel, Schema, Required
import pendulum
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.Desafio_Ponto
ponto_db = db["ponto"]
colaborador_db = db["colaborador"]

hour_format = "HH:mm:ss"
date_format = "DD/MM/YYYY"


class Ponto(BaseModel):
    colaborador_id: str = Schema(Required, title="Id colaborador do colaborador")
    # ponto_id: str = Schema(Required, title="Id colaborador do colaborador")
    # ponto_entrada: str = Schema(Required, title="Data e hora de registro do ponto na entrada.")
    # ponto_saida: str = Schema(None, title="Data e hora de registro do ponto do ponto da saída.")

    @classmethod
    def find(cls, ponto_id: str = None, colaborador_id: str = None, data: str = None, mes: str = None):
        where = {}
        where.update({"_id": f"{ponto_id.replace(' ', '')}"} if ponto_id else {})
        where.update({"data": f"{data.replace(' ', '')}"} if data else {})
        where.update({"colaborador_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})

        if mes:
            regex = re.compile(f"\d\d\/{mes.replace(' ', '')}\/\d\d\d\d")
            where.update({"data": regex})

        pontos = list(ponto_db.find(where).sort("data"))
        return pontos if ponto_db else None

    @classmethod
    def abrir_registro_ES(cls, colaborador_id):
        ponto_dict = {"_id": str(uuid1()),
                      "colaborador_id": colaborador_id,
                      "data": pendulum.now().format(date_format),
                      "registros_ES": [
                          {"_id": str(uuid1()), "entrada": pendulum.now().format(hour_format), "saida": ""}],
                      }
        return True if ponto_db.insert_one(ponto_dict) else False

    @classmethod
    def registrar_entrada(cls, ultimo_ponto):
        where = {"_id": ultimo_ponto["_id"]}
        registro_es = ultimo_ponto["registros_ES"]
        ultimo_registro = dict(registro_es[-1])
        if ultimo_registro['saida']:
            registro_es.append(
                {"_id": str(uuid1()), "entrada": pendulum.now().format(hour_format), "saida": ""})
            set = {"$set": {
                "registros_ES": registro_es,
            }}
            return True if ponto_db.update(where, set) else False
        return False

    @classmethod
    def registrar_saida(cls, ultimo_ponto):
        where = {"_id": ultimo_ponto["_id"]}
        registro_es = ultimo_ponto["registros_ES"]
        ultimo_registro = dict(registro_es.pop())
        if ultimo_registro['entrada']:
            ultimo_registro.update({"saida": pendulum.now().format(hour_format)})
            registro_es.append(ultimo_registro)
            set = {"$set": {
                "registros_ES": registro_es,
            }}
            return True if ponto_db.update(where, set) else False
        return False

    @classmethod
    def registrar_virada(cls, ultimo_ponto, colaborador_id):
        where = {"_id": ultimo_ponto["_id"]}
        registro_es = ultimo_ponto["registros_ES"]
        ultimo_registro = dict(registro_es.pop())
        if not ultimo_registro['saida']:
            ultimo_registro.update({"saida": "23:59:59"})
            registro_es.append(ultimo_registro)
            set = {"$set": {
                "registros_ES": registro_es,
            }}
            ponto_db.update(where, set)
            ponto_dict = {"_id": str(uuid1()),
                          "colaborador_id": colaborador_id,
                          "data": datetime.datetime.now().strftime(date_format),
                          "registros_ES": [{"_id": str(uuid1()),
                                            "entrada": "00:00:00",
                                            "saida": pendulum.now().format(hour_format)}],
                          }
            return True if ponto_db.insert_one(ponto_dict) else False
        return False

    @classmethod
    def remover(cls, ponto_id):
        where = {}
        where.update({"_id": f"{ponto_id}"} if ponto_id else {})

        if (not ponto_db.find(where)):
            return {'mensagem': "Ponto não encontrado para os parametroa informados."}

        if (ponto_db.delete_one(where)):
            return {'mensagem': "Ponto removido com sucesso."}

        return {'mensagem': "Problemas ao remover ponto."}
