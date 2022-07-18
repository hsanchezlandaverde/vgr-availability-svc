from typing import List

class AvailabilitiesRepository:

	def __init__(self):
		self.__availabilities = [
			{"id": 1, "name": "Available"},
			{"id": 2, "name": "Borrowed"},
			{"id": 3, "name": "Unavailable"},
			{"id": 4, "name": "Lost"},
			{"id": 5, "name": "Sold"},
		]

	def list(self) -> List:
		return self.__availabilities

	def findByID(self, id) -> dict:
		for availability in self.__availabilities:
			if availability['id'] == id:
				return availability
		return {}

	def create(self, name: str) -> int:
		next_id = self.__availabilities[len(self.__availabilities)-1]['id'] + 1
		self.__availabilities.append({"id": next_id, "name": name})
		return next_id

	def update(self, id, name) -> dict:
		for index, availability in enumerate(self.__availabilities):
			if availability['id'] == id:
				self.__availabilities[index]['name'] = name
				return self.__availabilities[index]

	def delete(self, id):
		for index, availability in enumerate(self.__availabilities):
			if availability['id'] == id:
				del self.__availabilities[index]
				return