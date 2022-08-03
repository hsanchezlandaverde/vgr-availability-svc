from typing import List
import psycopg2
from psycopg2 import Error
from log_utils import logger
from models import Availability

class AvailabilitiesRepository:

	__FIND_ALL_QUERY = "SELECT id, name, created_at, updated_at FROM availabilities ORDER BY id ASC"
	__FIND_BY_ID_QUERY = "SELECT id, name, created_at, updated_at FROM availabilities WHERE id = %d"
	__CREATE_QUERY = "INSERT INTO availabilities (name, created_at, updated_at) VALUES ('%s', '%s', '%s') RETURNING id;"
	__DELETE_BY_ID_QUERY = "DELETE FROM availabilities WHERE id = %d"
	__UPDATE_QUERY = "UPDATE availabilities SET name = '%s', updated_at = '%s' WHERE id = %d"

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

	def findAll(self) -> List:
		self.cursor.execute(self.__FIND_ALL_QUERY)
		records = self.cursor.fetchall()
		list = []
		for record in records:
			availability = Availability(record[0], record[1], record[2], record[3])
			list.append(availability.dict())
		return list

	def findByID(self, id) -> dict:
		self.cursor.execute(self.__FIND_BY_ID_QUERY % id)
		record = self.cursor.fetchone()
		if record == None:
			return {}
		availability = Availability(record[0], record[1], record[2], record[3])
		return availability.dict()

	def create(self, availability: Availability) -> int:
		try:
			self.cursor.execute(self.__CREATE_QUERY % (availability.name, availability.created_at, availability.updated_at))
		except:
			self.connection.rollback()
			return 0
		record = self.cursor.fetchone()
		self.connection.commit()
		return record[0]

	def update(self, availability: Availability) -> dict:
		try:
			self.cursor.execute(self.__UPDATE_QUERY % (availability.name, availability.updated_at, availability.id))
		except:
			self.connection.rollback()
			return None
		self.connection.commit()
		return self.findByID(availability.id)

	def delete(self, id):
		self.cursor.execute(self.__DELETE_BY_ID_QUERY % id)

	def __str__(self) -> str:
		return "PostgreSQL"