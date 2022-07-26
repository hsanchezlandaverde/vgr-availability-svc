import pytest
from app import server, validation_utils, repository

repositoryMock = repository.AvailabilitiesInMemoryRepository()

@pytest.fixture()
def app():
  app = server.create_server(validation_utils.Validator(), repositoryMock)
  app.config.update({
      "TESTING": True,
  })
  yield app

@pytest.fixture()
def client(app):
  return app.test_client()

@pytest.fixture()
def runner(app):
  return app.test_cli_runner()

def testNotFoundHandler(client):
  response = client.get("/v1/availabilities")
  assert response.status_code == 404

def testGetAll(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  response = client.get("/availabilities")
  assert response.status_code == 200
  assert response.json == [{"id":1,"name":"Available"},{"id":2,"name":"Borrowed"}]

def testGetById_GivenInvalidID_ReturnHTTP400(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.get("/availabilities/0")
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testGetById_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.get("/availabilities/4")
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 4"}}

def testGetById_WhenFound_ReturnHTTP200(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.get("/availabilities/2")
  assert response.status_code == 200
  assert response.json == {"id":2,"name":"Borrowed"}

def testCreate_GivenEmptyInput_ExpectHTTP400(client):
  repositoryMock.setup()
  response = client.post("/availabilities", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testCreate_GivenInvalidInput_ExpectHTTP400(client):
  repositoryMock.setup()
  response = client.post("/availabilities", json={"name":"foo"})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testCreate_GivenValidInput_ExpectHTTP201(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  response = client.post("/availabilities", json={"name":"Borrowed"})
  assert response.status_code == 201
  assert response.json == {"availability_id":2}
  
def testUpdate_GivenInvalidID_ReturnHTTP400(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.put("/availabilities/0", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testUpdate_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.put("/availabilities/4", json={})
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 4"}}

def testUpdate_GivenEmptyInput_ExpectHTTP400(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Pending...")
  response = client.put("/availabilities/3", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testUpdate_GivenInvalidInput_ExpectHTTP400(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Pending...")
  response = client.put("/availabilities/3", json={"name": "foo"})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testUpdate_GivenValidInput_ExpectHTTP200(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Pending...")
  response = client.put("/availabilities/3", json={"name": "Pending"})
  assert response.status_code == 200
  assert response.json == {"id":3,"name":"Pending"}


def testDelete_GivenInvalidID_ReturnHTTP400(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.delete("/availabilities/0")
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testDelete_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.delete("/availabilities/4")
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 4"}}

def testDelete_WhenSuccessfullyDeleted_ReturnHTTP204(client):
  repositoryMock.setup()
  repositoryMock.create("Available")
  repositoryMock.create("Borrowed")
  repositoryMock.create("Unavailable")
  response = client.delete("/availabilities/3")
  assert response.status_code == 204
  assert response.data == b''