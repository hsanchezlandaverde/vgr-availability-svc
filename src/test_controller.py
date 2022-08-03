import pytest
import mock
import server, validation_utils

repositoryMock = mock.Mock()

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
  repositoryMock.findAll.return_value = [
    {"id":1,"name":"Available","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"},
    {"id":2,"name":"Borrowed","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"},
  ]
  response = client.get("/availabilities")
  assert response.status_code == 200
  assert response.json == [
    {"id":1,"name":"Available","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"},
    {"id":2,"name":"Borrowed","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"},
  ]

def testGetById_GivenInvalidID_ReturnHTTP400(client):
  response = client.get("/availabilities/0")
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testGetById_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.findByID.return_value = {}
  response = client.get("/availabilities/8")
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 8"}}

def testGetById_WhenFound_ReturnHTTP200(client):
  repositoryMock.findByID.return_value = {"id":2,"name":"Borrowed","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  response = client.get("/availabilities/2")
  assert response.status_code == 200
  assert response.json == {"id":2,"name":"Borrowed","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}

def testCreate_GivenEmptyInput_ExpectHTTP400(client):
  response = client.post("/availabilities", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testCreate_GivenInvalidInput_ExpectHTTP400(client):
  response = client.post("/availabilities", json={"name":"foo"})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testCreate_GivenValidInput_ExpectHTTP201(client):
  repositoryMock.create.return_value = 2
  response = client.post("/availabilities", json={"name":"Borrowed"})
  assert response.status_code == 201
  assert response.json == {"availability_id":2}

def testUpdate_GivenInvalidID_ReturnHTTP400(client):
  response = client.put("/availabilities/0", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testUpdate_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.findByID.return_value = {}
  response = client.put("/availabilities/8", json={})
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 8"}}

def testUpdate_GivenEmptyInput_ExpectHTTP400(client):
  repositoryMock.findByID.return_value = {"id":4,"name":"Lost","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  response = client.put("/availabilities/3", json={})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testUpdate_GivenInvalidInput_ExpectHTTP400(client):
  repositoryMock.findByID.return_value = {"id":3,"name":"Unavailable","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  response = client.put("/availabilities/3", json={"name": "foo"})
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [name] must be at least 4 characters"}}

def testUpdate_WhenConflictOccurs_ExpectHTTP409(client):
  repositoryMock.findByID.return_value = {"id":6,"name":"Pending...","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  repositoryMock.update.return_value = None
  response = client.put("/availabilities/3", json={"name": "Pending"})
  assert response.status_code == 409

def testUpdate_GivenValidInput_ExpectHTTP200(client):
  repositoryMock.findByID.return_value = {"id":6,"name":"Pending...","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  repositoryMock.update.return_value = {"id":6,"name":"Pending","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  response = client.put("/availabilities/6", json={"name": "Pending"})
  assert response.status_code == 200
  assert response.json == {"id":6,"name":"Pending","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}

def testDelete_GivenInvalidID_ReturnHTTP400(client):
  response = client.delete("/availabilities/0")
  assert response.status_code == 400
  assert response.json == {"error":{"message":"Parameter [id] must be a positive integer"}}

def testDelete_WhenNotFound_ReturnHTTP404(client):
  repositoryMock.findByID.return_value = {}
  response = client.delete("/availabilities/8")
  assert response.status_code == 404
  assert response.json == {"error":{"message":"No availability found with [id]: 8"}}

def testDelete_WhenSuccessfullyDeleted_ReturnHTTP204(client):
  repositoryMock.findByID.return_value = {"id":6,"name":"Pending","created_at":"2022-08-01 12:00:00","updated_at":"2022-08-01 12:00:00"}
  repositoryMock.delete.return_value = None
  response = client.delete("/availabilities/6")
  assert response.status_code == 204
  assert response.data == b''
