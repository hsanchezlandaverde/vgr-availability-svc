# vgr-availability-svc

## Setup

  - Install Python version `3.8`+
  - Download dependencies with the command `pip install -r requirements.txt`
  - Configure the next environment variables:
    - `SERVER_HOST` the host address to listen (defaults to 0.0.0.0).
    - `SERVER_PORT` the TCP port to listen (defaults to 8092).
    - `SERVER_DEBUG` set to `true` for enable debug, `false` (default) otherwise.
    - `DB_HOST` the database (Postgres) host address without port to connect..
    - `DB_PORT` the database port to connect.
    - `DB_NAME` the database name to connect.
    - `DB_USER` the database user to connect.
    - `DB_PASSWORD` the database password to connect.
  - *NOTE*: If no _`DB_*`_ environment variables are set, the service will run in volatile mode with an in-memory database.
  - Run the command `python app.py`
  - App will run on `http://localhost:8092`
  - A complete [**swagger.yml**](./docs/swagger.yml) definition is provided to test the available endpoints.

## Docker

Build docker image:

    docker build -t vgr-availability-svc:latest .

Run docker container:

    docker run -d -p 8092:8092 -e DB_HOST="" -e DB_PORT="" -e DB_NAME="" -e DB_USER="" -e DB_PASSWORD="" --name vgr-availability-svc vgr-availability-svc:latest