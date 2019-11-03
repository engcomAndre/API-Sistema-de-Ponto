import re
from uuid import uuid1
from pydantic import BaseModel, Schema, Required
import pendulum
from db.db import Db

hour_format = "HH:mm:ss"
date_format = "DD/MM/YYYY"


class Ponto(BaseModel):
    _id: str = Schema(None, title="Id colaborador do colaborador")
    colaborador_id: str = Schema(Required, title="Id colaborador do colaborador")
    data: str = Schema(None, title="Data do Ponto", description="Data de registro do ponto")
    registros_ES: list = Schema([], title='Registro de entrada e saída.', description="Registro de entrada e saída.")

    @classmethod
    def find(cls, ponto_id: str = None, colaborador_id: str = None, data: str = None, mes: str = None) -> list:
        try:
            where = {}
            where.update({"_id": f"{ponto_id.replace(' ', '')}"} if ponto_id else {})
            where.update({"data": f"{data.replace(' ', '')}"} if data else {})
            where.update({"colaborador_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})

            if mes:
                regex = re.compile(f"\d\d\/{mes.replace(' ', '')}\/\d\d\d\d")
                where.update({"data": regex})

            pontos = Db.find("ponto", where, sort_by="data")

            return pontos if pontos else None
        except:
            # TODO EXCEPT
            return []

    def registrar_virada_in(self) -> bool:
        try:
            res = False
            res = self.registrar_saida_in("23:59:59")
            res = self.criar_registro_ES(hour_in='00:00:00', hour_out=pendulum.now().format(hour_format))
            return res
        except:
            # TODO EXCEPT
            return False

    def criar_registro_ES(self, hour_in: str = None, hour_out: str = "") -> bool:
        try:
            self.data = pendulum.now().format(date_format)
            self.registros_ES = []
            self.registros_ES = [
                {"_id": str(uuid1()), "entrada": hour_in if hour_in else pendulum.now().format(hour_format),
                 "saida": hour_out if hour_out else ""}]
            return True if Db.save('ponto', self) else False
        except:
            # TODO EXCEPT
            return False

    def e_virada(self) -> bool:
        try:
            if not self.data:
                return False
            dif_dias = pendulum.period(pendulum.from_format(self.data, date_format), pendulum.now()).in_days()
            if dif_dias > 0 and self.registros_ES[-1]['saida'] == "":
                return True
            return False
        except:
            # TODO EXCEPT
            return False

    def e_entrada(self) -> bool:
        try:
            if not self.data:
                return True

            if self.registros_ES[-1]['saida'] != '':
                return True

            dif_dias = pendulum.period(pendulum.from_format(self.data, date_format), pendulum.now()).in_days()
            if dif_dias >= 0 and self.registros_ES[-1]["saida"] != "":
                return True
            return False
        except:
            # TODO EXCEPT
            return False

    def registrar_entrada_in(self, hour: str = None) -> bool:
        try:
            if not self.data:
                return self.criar_registro_ES()

            dif_dias = pendulum.period(pendulum.from_format(self.data, date_format), pendulum.now()).in_days()
            if dif_dias > 0 and self.registros_ES[-1]["saida"] != "":
                return self.criar_registro_ES()

            where = {"colaborador_id": self.colaborador_id, "data": self.data}
            self.registros_ES.append(
                {"_id": str(uuid1()), "entrada": pendulum.now().format(hour_format) if not hour else hour
                    , "saida": ""})
            return True if Db.update("ponto", where, self) else False
        except:
            # TODO EXCEPT
            return False

    def registrar_saida_in(self, hora: str = None) -> bool:
        try:
            where = {"data": self.data, "colaborador_id": self.colaborador_id}
            self.registros_ES[-1].update({"saida": hora if hora else pendulum.now().format(hour_format)})
            return True if Db.update("ponto", where, self) else False
        except:
            # TODO EXCEPT
            return False

    def remover(self) -> bool:
        try:
            return Db.delete('ponto',self)
        except:
            # TODO EXCEPT
            return False
