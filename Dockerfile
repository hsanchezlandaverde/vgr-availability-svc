# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

ENV DEBUG_ENABLED=true

ENV PORT=8092

EXPOSE 8092

CMD ["python3", "app.py"]
