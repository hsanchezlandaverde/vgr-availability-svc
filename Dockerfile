# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /vgr-availability-svc

COPY src app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV FLASK_ENV=development

ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8092
ENV SERVER_DEBUG=false

EXPOSE 8092

CMD ["python3", "app"]
