from configuration import Configuration
from validation_utils import Validator
from repository import AvailabilitiesRepository
from log_utils import logger
from server import create_server

# 'dependency injection'
config = Configuration().fromEnv()
logger.debug("using configuration: %s", config)

validator = Validator()
logger.debug("using validator: %s", validator)

repository = None
if config.isDatabaseConfigured():
  repository = AvailabilitiesRepository(config)
  logger.debug("using repository: %s", repository)
else:
  logger.error("database not configured.")

server = create_server(validator, repository)
server.run(host=config.server_host, port=config.server_port, debug=config.server_debug)
