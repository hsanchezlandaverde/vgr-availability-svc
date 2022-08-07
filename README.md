# vgr-availability-svc

## Setup

  - Install Python version `3.8`+
  - Download dependencies with the command `pip install -r requirements.txt`
  - Configure PostgreSQL database. You can use also a docker image to run the postgres container. After, you can use [Flyway](https://flywaydb.org/) to run the migrations located under the `./sql` folder (please create database before run flyway commands).
  - Configure the next environment variables (mandatory):
    - `SERVER_HOST` the host address to listen (defaults to 0.0.0.0).
    - `SERVER_PORT` the TCP port to listen (defaults to 8092).
    - `SERVER_DEBUG` set to `true` for enable debug, `false` (default) otherwise.
    - `DB_HOST` the database (PostgreSQL) host address without port to connect..
    - `DB_PORT` the database (PostgreSQL) port to connect.
    - `DB_NAME` the database (PostgreSQL) name to connect.
    - `DB_USER` the database (PostgreSQL) user to connect.
    - `DB_PASSWORD` the database (PostgreSQL) password to connect.
  - Run the command `python app.py`
  - App will run on `http://localhost:8092`
  - A complete [**swagger.yml**](./docs/swagger.yml) definition is provided to test the available endpoints, you could import it with Insomnia Core or Postman.

## Testing

In order to test, you can install the next packages:

    pip install pytest --user
    pip install pytest-cov --user

Use the next command to run the unit tests:

    python -m pytest -v

Use the next command to run unit tests with coverage:

    python -m pytest --cov-report term-missing --cov

### Coverage

```
-------------------------------------------
Name                    Stmts   Miss  Cover
-------------------------------------------
__init__.py                 0      0   100%
configuration.py           35     15    57%
models.py                  11      0   100%
req_utils.py                4      0   100%
res_utils.py               41      2    95%
server.py                  61      0   100%
test_configuration.py      42      0   100%
test_controller.py         95      1    99%
test_model.py              12      0   100%
test_validator.py          25      0   100%
validation_utils.py        11      0   100%
-------------------------------------------
TOTAL                     337     18    95%
```

## Docker

Build docker image:

    docker build -t vgr-availability-svc:latest .

Run docker container:

    docker run -d -p 8092:8092 -e DB_HOST="host.docker.internal" -e DB_PORT="" -e DB_NAME="vgr_availability" -e DB_USER="" -e DB_PASSWORD="" --name vgr-availability-svc vgr-availability-svc:latest

## ToDo

- [ ] Write logs to file in order to troubleshoot.
- [ ] Run flyway migrations with Docker.
- [ ] Check out for **fastAPI** migration.