### Api Sistema de Ponto
Este repositório e de uma API de  Sistema de Ponto como atividade sugestão de desafio no processo seletivo da Empresa PontoTel.

#### Motivação e Descrição
Para maiores detalhes acesse ,[PONTO TEL DESAFIO - Sistema de Ponto](https://drive.google.com/open?id=1DooIrnWJPQVIswpNDMvVerJH-478HD0j)


#### Caracteristicas
- [API](https://pt.wikipedia.org/wiki/Interface_de_programa%C3%A7%C3%A3o_de_aplica%C3%A7%C3%B5es "API")
- [Python > 3.6](https://www.python.org/)
- [Flask](http://flask.palletsprojects.com/en/1.1.x/ "Flask")
- [FastApi](https://fastapi.tiangolo.com/features/ "FastApi")
- [Mongo](https://www.mongodb.com "mongo")
- [Pytest](https://docs.pytest.org/en/latest/getting-started.html "Pytest")
- [Docker](https://www.docker.com "Docker")


### Rodando a aplicação com Docker-Compose
Rode os comandos;
#### Compilando o projeto (Build)
`$ sudo docker-compose build`
#### Subindo a aplicação (Up)
`$ sudo docker-compose up`

### Rodando sem Docker
#### Instale os programa e requisitos necessários: 
- MongoDB(versão 3.6),
- Python (versão 3.6 ou superior),
- Mongo Compass(Sugestão).

#### Siga os passos abaixo:

###### 1.Clone este repositório
 ```
`$git clone https://github.com/engcomAndre/Sistema-de-Ponto.git`
 ```

###### 2. Inicie o ambiente virtual(venv,pipenv...),para mais detalhes sobre o assunto acesse abaixo:

 [Como programaar em ambientes virtuais com python.](https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais)

 ###### 3. Instale os bibliotecas necessárias.

 - Rode o comando na raiz do projeto :
`$ python run.py`


### Documentação
Após subir a aplicação a documentação estará disponível no endereço:

`[URL_BASE]/redoc` 

ou

`[URL_BASE]/docs`

Uma imagem similar a abaixo deverá ser mostrado no seu navegador :

[![Swager Docs](https://i.imgur.com/WZm9Wjc.png "Swager Docs")](http://imgur.com/WZm9Wjc "Swager Docs")

ou se preferir ,acesse: [<b>Swagger Editor</b>](https://editor.swagger.io) e faça  e upload do arquivo <b>swagger_api_doc.json</b>.

### Testes
Os testes foram realizados com o runner [<b>pytest</b>](https://docs.pytest.org/en/latest/) ,é necessário que ele esteja instalado em seu ambiente para executar os testes.
Existem várias formas de executa-los ,a mais simples e através da IDE [Pycharm](https://www.jetbrains.com/pycharm/).
Basicamente,faça:
1.Acesse a Guia File -> Settings,
2.Selecione <b>Tools</b> e em <b>Python Integrated Tools</b> e em <b>Testing</b> no campo <b>default test runner</b> selecione <b>pytest</b>.
3.Clique com o botão direito sobre a pasta <b>tests</b> e na guia que abrir selecione <b>Run pytest in tests</b>.
