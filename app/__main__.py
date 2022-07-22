from configuration import Configuration
from validation_utils import Validator
from repository import AvailabilitiesInMemoryRepository, AvailabilitiesSQLRepository
from log_utils import logger
from server import create_server

# 'dependency injection'
config = Configuration().fromEnv()
logger.debug("using configuration: %s", config)

validator = Validator()
logger.debug("using validator: %s", validator)

repository = {}
if config.isDatabaseConfigured():
  repository = AvailabilitiesSQLRepository(config)
else:
  repository = AvailabilitiesInMemoryRepository()
logger.debug("using repository: %s", repository)

server = create_server(validator, repository)
server.run(host=config.server_host, port=config.server_port, debug=config.server_debug)
