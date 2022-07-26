from typing import List
import psycopg2
from psycopg2 import Error
import sys
from app.log_utils import logger

class AvailabilitiesInMemoryRepository:

	def __init__(self):
		self.__availabilities = [
			{"id": 1, "name": "Available"},
			{"id": 2, "name": "Borrowed"},
			{"id": 3, "name": "Unavailable"},
			{"id": 4, "name": "Lost"},
			{"id": 5, "name": "Sold"},
		]

	def findAll(self) -> List:
		return self.__availabilities

	def findByID(self, id) -> dict:
		for availability in self.__availabilities:
			if availability['id'] == id:
				return availability
		return {}

	def create(self, name: str) -> int:
		next_id = 1
		if len(self.__availabilities) > 0:
			next_id = self.__availabilities[len(self.__availabilities)-1]['id'] + 1
		self.__availabilities.append({"id": next_id, "name": name})
		return next_id

	def update(self, id, name) -> dict:
		for index, availability in enumerate(self.__availabilities):
			if availability['id'] == id:
				self.__availabilities[index]['name'] = name
				return self.__availabilities[index]

	def delete(self, id) -> bool:
		for index, availability in enumerate(self.__availabilities):
			if availability['id'] == id:
				del self.__availabilities[index]
				return

	# made for unit testing
	def setup(self):
		self.__availabilities = []

	def __str__(self) -> str:
		return "in-memory.volatile.database"

class AvailabilitiesSQLRepository:

	__FIND_ALL_QUERY = "SELECT id, name FROM availabilities ORDER BY id ASC"
	__FIND_BY_ID_QUERY = "SELECT id, name FROM availabilities WHERE id = %d"
	__CREATE_QUERY = "INSERT INTO availabilities (name) VALUES ('%s') RETURNING id;"
	__DELETE_BY_ID_QUERY = "DELETE FROM availabilities WHERE id = %d"
	__UPDATE_QUERY = "UPDATE availabilities SET name = '%s' WHERE id = %d"

	def __init__(self, config):
		try:
			self.connection = psycopg2.connect(host=config.db_host, port=config.db_port,
			database=config.db_name, user=config.db_user, password=config.db_password)
			self.cursor = self.connection.cursor()
			logger.debug(self.connection.get_dsn_parameters())
			self.cursor.execute("SELECT version();")
			record = self.cursor.fetchone()
			logger.debug("connected to - %s", record)
		except (Exception, Error) as error:
			logger.error("error while connecting to PostgreSQL: %s", error)
			logger.error("service will now exit.")
			sys.exit(-1)

	def findAll(self) -> List:
		self.cursor.execute(self.__FIND_ALL_QUERY)
		records = self.cursor.fetchall()
		list = []
		for record in records:
			list.append({"id": record[0], "name": record[1]})
		return list

	def findByID(self, id) -> dict:
		self.cursor.execute(self.__FIND_BY_ID_QUERY % id)
		record = self.cursor.fetchone()
		if record == None:
			return {}
		return {"id": record[0], "name": record[1]}

	def create(self, name: str) -> int:
		self.cursor.execute(self.__CREATE_QUERY % name)
		record = self.cursor.fetchone()
		self.connection.commit()
		return record[0]

	def update(self, id, name) -> dict:
		self.cursor.execute(self.__UPDATE_QUERY % (name, id))
		self.connection.commit()
		return self.findByID(id)

	def delete(self, id):
		self.cursor.execute(self.__DELETE_BY_ID_QUERY % id)

	def __str__(self) -> str:
		return "PostgreSQL"