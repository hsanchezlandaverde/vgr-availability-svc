from flask import Flask, request
from datetime import datetime, timezone
from configuration import APP_NAME
from validation_utils import Validator
from req_utils import GET_METHOD, PUT_METHOD, POST_METHOD, DELETE_METHOD
from res_utils import *

# @TODO check for https://fastapi.tiangolo.com/tutorial/first-steps/

def create_server(valid: Validator, repository):
	server = Flask(APP_NAME)
	server.register_error_handler(HTTP_NOT_FOUND, notFoundHandler)
	server.register_error_handler(HTTP_INTERNAL_SERVER_ERROR, internalServerErrorHandler)
	server.config["JSON_SORT_KEYS"] = False

	# GET /availabilities
	# Gets all the existing availabilities.
	# @version 1.0
	@server.route("/availabilities", methods=[GET_METHOD])
	def getAll():
		return ok(repository.findAll())

	# GET /availabilities/<id>
	# Get an availability by its ID.
	# @version 1.0
	@server.route("/availabilities/<int:id>", methods=[GET_METHOD])
	def getById(id):
		if not valid.id(id):
			return badRequest(INVALID_ID_COPY)
		availability = repository.findByID(id)
		if not valid.availability(availability):
			return notFound(AVAILABILITY_NOTFOUND_COPY % id)
		return ok(availability)

	# POST /availabilities
	# Creates a new availability.
	# @version 1.0
	@server.route("/availabilities", methods=[POST_METHOD])
	def create():
		if request.json == {}:
			return badRequest(INVALID_NAME_COPY)
		name = request.json["name"]
		if not valid.name(name):
			return badRequest(INVALID_NAME_COPY)
		created_at = updated_at = datetime.now(timezone.utc)
		availability = Availability(id, name, created_at, updated_at)
		next_id = repository.create(availability)
		return created(next_id)

	# PUT /availabilities/<id>
	# Updates an existing availability by its ID.
	# @version 1.0
	@server.route("/availabilities/<int:id>", methods=[PUT_METHOD])
	def update(id):
		if not valid.id(id):
			return badRequest(INVALID_ID_COPY)
		availability = repository.findByID(id)
		if not valid.availability(availability):
			return notFound(AVAILABILITY_NOTFOUND_COPY % id)
		if request.json == {}:
			return badRequest(INVALID_NAME_COPY)
		name = request.json["name"]
		if not valid.name(name):
			return badRequest(INVALID_NAME_COPY)
		updated_at = datetime.now(timezone.utc)
		availability = Availability(id, name, None, updated_at)
		availability = repository.update(availability)
		if availability is None:
			return conflict(name)
		return ok(availability)

	# DELETE /availabilities/<id>
	# Deletes an existing availability by its ID.
	# @version 1.0
	@server.route("/availabilities/<int:id>", methods=[DELETE_METHOD])
	def deleteById(id):
		if not valid.id(id):
			return badRequest(INVALID_ID_COPY)
		availability = repository.findByID(id)
		if not valid.availability(availability):
			return notFound(AVAILABILITY_NOTFOUND_COPY % id)
		repository.delete(id)	
		return noContent()

	return server
