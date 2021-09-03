from flask import Flask, abort, request
from configuration import Configuration
from requests import *
from responses import *
from repository import AvailabilitiesRepository
from validator import Validator

app = Flask(__name__)
configuration = Configuration().fromEnv()
repository = AvailabilitiesRepository()
valid = Validator()

# GET /availabilities
# Gets all the existing availabilities.
# @version 1.0
@app.route('/availabilities', methods=[GET_METHOD])
def readAll():
	return ok(repository.list())

# GET /availabilities/<id>
# Get an availability by its id.
# @version 1.0
@app.route('/availabilities/<int:id>', methods=[GET_METHOD])
def readById(id):
	if not valid.id(id):
		return badRequest(INVALID_ID_COPY)
	availability = repository.findByID(id)
	if not valid.availability(availability):
		return notFound(AVAILABILITY_NOTFOUND_COPY % id)
	return ok(availability)

# POST /availabilities
# Creates a new availability.
# @version 1.0
@app.route('/availabilities', methods=[POST_METHOD])
def create():
	name = request.json['name']
	if not valid.name(name):
		return badRequest(INVALID_NAME_COPY)
	next_id = repository.create(name)
	return created(next_id)

# PUT /availabilities/<id>
# Updates an existing availability by its id.
# @version 1.0
@app.route('/availabilities/<int:id>', methods=[PUT_METHOD])
def update(id):
	if not valid.id(id):
		return badRequest(INVALID_ID_COPY)
	name = request.json['name']
	if not valid.name(name):
		return badRequest(INVALID_NAME_COPY)
	availability = repository.update(id, name)
	if not valid.availability(availability):
		return notFound(AVAILABILITY_NOTFOUND_COPY % id)
	return ok(availability)

# DELETE /availabilities/<id>
# Deletes an existing availability by its id.
# @version 1.0
@app.route('/availabilities/<int:id>', methods=[DELETE_METHOD])
def deleteById(id):
	if not valid.id(id):
		return badRequest(INVALID_ID_COPY)
	availability = repository.findByID(id)
	if not valid.availability(availability):
		return notFound(AVAILABILITY_NOTFOUND_COPY % id)
	repository.delete(id)
	return noContent()

if __name__ == '__main__':
	app.register_error_handler(HTTP_NOT_FOUND, notFoundHandler)
	app.register_error_handler(HTTP_INTERNAL_SERVER_ERROR, internalServerErrorHandler)
	app.run(debug=configuration.debug, port=configuration.port)