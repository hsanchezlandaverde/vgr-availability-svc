from flask import jsonify, Response
from models import Availability

INVALID_ID_COPY = "Parameter [id] must be a positive integer"
INVALID_NAME_COPY = "Parameter [name] must be at least 4 characters"
AVAILABILITY_NOTFOUND_COPY = "No availability found with [id]: %d"
CONFLICT_COPY = "A conflict ocurred with processing request: [name]: '%s' already exists"

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_INTERNAL_SERVER_ERROR = 500

def notFoundHandler(obj):
	return notFound(str(obj))

def internalServerErrorHandler(obj):
	return internalServerError(str(obj))

def errorResponse(status_code: int, message: str):
	response = jsonify({
		"error": {
			"message": message
		}
	})
	response.status_code = status_code
	return response

def ok(obj) -> Response:
	response = jsonify(obj)
	response.status_code = HTTP_OK
	return response

def created(availability_id: int):
	response = jsonify({
		"availability_id": availability_id
	})
	response.status_code = HTTP_CREATED
	return response

def noContent():
	response = jsonify({})
	response.status_code = HTTP_NO_CONTENT
	return response

def badRequest(message):
	return errorResponse(HTTP_BAD_REQUEST, message)

def notFound(message):
	return errorResponse(HTTP_NOT_FOUND, message)

def conflict(name):
	return errorResponse(HTTP_CONFLICT, CONFLICT_COPY % name)

def internalServerError(message):
	return errorResponse(HTTP_INTERNAL_SERVER_ERROR, message)
