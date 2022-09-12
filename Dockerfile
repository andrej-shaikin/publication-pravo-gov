FROM python:3.10-slim-buster

MAINTAINER Andrey Shaikin <kiwibon@yandex.ru>

ENV PROJECT_DIR=/app
USER root

WORKDIR $PROJECT_DIR

COPY requirements requirements
RUN pip install -r requirements/main.txt -r requirements/dev.txt

COPY .flake8 .flake8
COPY app.py app.py
COPY apps apps
COPY conf conf
