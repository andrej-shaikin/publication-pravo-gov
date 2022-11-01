FROM python:3.10-slim-buster

MAINTAINER Andrey Shaikin <kiwibon@yandex.ru>

ENV PROJECT_DIR=/app
WORKDIR $PROJECT_DIR
USER root

RUN apt update && apt install git python3-dev build-essential -y
COPY requirements requirements
RUN pip install --no-cache-dir -r requirements/main.txt -r requirements/dev.txt

COPY .flake8 app.py ./
COPY apps apps
COPY conf conf
COPY scripts scripts
RUN chmod +x scripts/*.sh

EXPOSE 80
