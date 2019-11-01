# Imagem Base
FROM python:3.7.3

# Informações sobre esta imagem
LABEL version="1.0" description="API de um Sistema de Ponto" maintainer="Andre Vieira da Silva" email="sgavsnake@gmail.com"

# Endereço onde ficará a nossa API
ENV APP=/usr/src/app

# Criando a pasta onde ficará a aplicação
RUN mkdir -p $APP

# Copiando todos os arquivos para dentro do container
COPY . $APP

# Ponto de entrada para execução de qualquer instrução
WORKDIR $APP

# Instalando as dependências
RUN pip3 install -r requirements.txt

# Expondo a porta
EXPOSE 8000

# Executando nossa aplicação
CMD python3 run.py