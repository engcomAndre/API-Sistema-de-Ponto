from api.models.ColaboradorModel import Colaborador
from api.models.PontoModel import Ponto

col1 = Colaborador(nome="col_001", endereco="end_col_001", cpf='11111111111')
col2 = Colaborador(nome="col_002", endereco="end_col_002", cpf='22222222222')
col3 = Colaborador(nome="col_003", endereco="end_col_003", cpf='33333333333')

ponto1 = Ponto(colaborador_id="11111111111")
ponto2 = Ponto(colaborador_id="22222222222")
