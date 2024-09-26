FROM python:3.12.3-alpine3.19

RUN pip install poetry

COPY https://github.com/PJIgrupo004/ProjetoIntegrador1.git /opt/webserver

WORKDIR /opt/webserver/Site

RUN poetry install

EXPOSE 5000

ENTRYPOINT [ "/bin/bash", "poetry run flask run --host 0.0.0.0 --port 5000" ]
