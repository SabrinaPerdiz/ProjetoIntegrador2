# Projeto integrador I - UNIVESP
Website para a disciplina "Projeto integrado II" da UNIVESP (diversos cursos no eixo de computação)

## Descrição
Site para salão de beleza contemplando as seguintes funcionalidades:

[ ] Cadastro de clientes<br>
[ ] Tela do cliente para ver as solicitações atuais e passadas<br>
[ ] Cadastro de serviços<br>
[ ] Cadastro de posts do Intagram para presentação na tela inicial<br>
[ ] Formulário de solicitação de agendamento<br>
[ ] Tela de administrador para visualização e edição dos cadastros<br>

## Alunos participantes

Diana Alves, RA: 2207712<br>
Elder Fernandes de Oliveira, RA: 2221701<br>
Isaac Souza dos Anjos, RA: 2229397<br>
Jéssica Caroline Oliveira de Jesus, RA: 2213596<br>
Milene Teixeira Cabrini, RA: 2217974<br>
<a href="https://github.com/SabrinaPerdiz" target="_blank">Sabrina Mai Nakaichi Perdiz, RA: 2212338</a><br>
Sérgio Rodrigo Costa, RA: 2208035<br>
<a href="https://github.com/Tiagots23" target="_blank"> Tiago Tavares da Silva, RA: 2208690</a><br>

## Como instalar

Execute os comandos abaixo:

```sh
pip install poetry

cd site

poetry install
```

## Como executar

Para subir o serviço localmente, execute no terminal o seguinte comando:

```sh
cd site

poetry run flask run --host 0.0.0.0 --port 5000
```

## Configurar o banco de dados

- Criar a base no mysql com o nome desejado;
- Executar as DDL's do arquivo Banco_de_dados/banco_de_dados.sql;
- Duplicar o arquivo db_connection_data_mockup.py;
- Preencher as variáveis conforme o orientado;
- Alterar o nome do arquivo duplicado para db_connection_data.py.

OBS: feito dessa maneira para proteger os dados de acesso, o arquivo db_connection_data.py já está incluso no gitignore