import re
from uuid import uuid1
from pydantic import BaseModel, Schema, Required
import pendulum
from typing import List, Dict, Tuple

from utils.time_utils import date_format, hour_format, format_date
from db.db import Db


class Ponto(BaseModel):
    _id: str = Schema(None, title="Id unico do colaborador")
    colaborador_id: str = Schema(Required, title="Id colaborador do colaborador")
    data: str = Schema(None, title="Data do Ponto", description="Data de registro do ponto formato DD/MM/YYYY",
                       regex="\\d\\d\\/\\d\\d\\/\\d\\d\\d\\d")
    registros_ES: List[Dict[str, str]] = Schema([], title='Registro de entrada e saída.',
                                                description="Registro de entrada e saída .")

    def save(self) -> Dict[str, str]:
        try:
            ret = Db.save('ponto', self)
            return ret
        except:
            raise Exception

    @classmethod
    def find(cls, ponto_id: str = None, colaborador_id: str = None, data: str = None, mes: str = None) -> List[
        Dict[str, str]]:
        try:
            where = {}
            where.update({"_id": f"{ponto_id.replace(' ', '')}"} if ponto_id else {})
            where.update({"data": f"{data.replace(' ', '')}"} if data else {})
            where.update({"colaborador_id": f"{colaborador_id.replace(' ', '')}"} if colaborador_id else {})

            if mes:
                regex = re.compile(f"\\d\\d\\/{mes.replace(' ', '')}\\/\\d\\d\\d\\d")
                where.update({"data": regex})

            pontos = Db.find("ponto", where, sort_by="data")

            return pontos if pontos else None
        except:
            raise Exception

    def registrar_virada_in(self) -> bool:
        try:
            res = False
            res = self.registrar_saida_in("23:59:59")
            res = self.criar_registro_ES(hour_in='00:00:00', hour_out=pendulum.now().format(hour_format))
            return True if res else False
        except:
            # TODO EXCEPTION
            raise Exception

    def criar_registro_ES(self, hour_in: str = None, hour_out: str = "") -> Dict[str, str]:
        try:
            self.data = pendulum.now().format(date_format)
            self.registros_ES = []
            self.registros_ES = [
                {"_id": str(uuid1()), "entrada": hour_in if hour_in else pendulum.now().format(hour_format),
                 "saida": hour_out if hour_out else ""}]
            ret = Db.save('ponto', self)
            return ret if ret else None
        except:
            raise Exception
            # TODO EXCEPTION

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
            raise Exception

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
            raise Exception

    def registrar_entrada_in(self, hour: str = None) -> bool:
        try:
            if not self.data:
                return True if self.criar_registro_ES() else False

            dif_dias = pendulum.period(pendulum.from_format(self.data, date_format), pendulum.now()).in_days()
            if dif_dias > 0 and self.registros_ES[-1]["saida"] != "":
                return True if self.criar_registro_ES() else False

            where = {"colaborador_id": self.colaborador_id, "data": self.data}
            self.registros_ES.append(
                {"_id": str(uuid1()), "entrada": pendulum.now().format(hour_format) if not hour else hour
                    , "saida": ""})
            return True if Db.update("ponto", where, self) else False
        except:
            # TODO EXCEPT
            raise Exception

    def registrar_saida_in(self, hora: str = None) -> bool:
        try:
            where = {"data": self.data, "colaborador_id": self.colaborador_id}
            self.registros_ES[-1].update({"saida": hora if hora else pendulum.now().format(hour_format)})
            return True if Db.update("ponto", where, self) else False
        except:
            raise Exception
            # TODO EXCEPT

    def remover(self) -> bool:
        try:
            return Db.delete('ponto', self)
        except:
            raise Exception
            # TODO EXCEPT

    def calcular_horas_dias(self) -> Tuple[int, List[Dict[str, str]]]:
        try:
            output = []
            t_duracao_dia = 0
            for io in self.registros_ES:
                try:
                    h_saida = pendulum.parse(io["saida"]) if io["entrada"] else None
                    h_entrada = pendulum.parse(io["entrada"]) if io["saida"] else None

                    period = pendulum.period(h_entrada, h_saida).in_seconds()
                    t_duracao_dia += period
                except:
                    output.append({"Data": self.data,
                                   "Horas Trabalhadas no dia": "Registros com problemas ,não considerado para os cálculos"})
                    pass
            output.append({"Data": self.data, "Horas Trabalhadas no dia": format_date(t_duracao_dia)})

            return t_duracao_dia, output
        except:
            raise Exception
            ##TODO EXCEPTION

    @classmethod
    def calcular_horas_mes(cls, pontos_mes: list) -> Tuple[int, Dict[str, str]]:
        try:
            output = []
            t_mes = 0
            for ponto in pontos_mes:
                ponto = Ponto(**ponto)
                t_dia, t_res = ponto.calcular_horas_dias()
                output.append(t_res[0])
                t_mes += t_dia
            return t_mes, {"Total de tempo Trabalhado no mês": format_date(t_mes), "Totais de tempo por dia": output}
        except:
            raise Exception
            # TODO EXCEPTION
