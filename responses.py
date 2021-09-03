from flask import jsonify

INVALID_ID_COPY = "Parameter 'id' must be a positive integer"
INVALID_NAME_COPY = "Parameter 'name' must be at least 4 characters"
AVAILABILITY_NOTFOUND_COPY = "No availability found with 'id': %d"

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500

def ok(obj):
	response = jsonify(obj)
	response.status_code = HTTP_OK
	return response

def created(availability_id: int):
	response = jsonify({
		'availability_id': availability_id
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

def internalServerError(message):
	return errorResponse(HTTP_INTERNAL_SERVER_ERROR, message)

def errorResponse(status_code: int, message: str):
	response = jsonify({
		'error': {
			'message': message
		}
	})
	response.status_code = status_code
	return response

def notFoundHandler(obj):
	return notFound(str(obj))

def internalServerErrorHandler(obj):
	return internalServerError(str(obj))