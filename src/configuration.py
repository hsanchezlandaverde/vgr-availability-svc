import os

APP_NAME = "vgr-availability-svc"
APP_VERSION = "1.4.0"

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8092

class Configuration:

  def __init__(self):
    self.server_host = DEFAULT_HOST
    self.server_port = DEFAULT_PORT
    self.server_debug = False
    self.db_host = None
    self.db_port = None
    self.db_name = None
    self.db_user = None
    self.db_password = None

  def __str__(self):
    return """{ server_host: %s, server_port: %d, server_debug: %s, db_host: %s, db_port: %s, db_name: %s, db_user: %s, db_password: %s }""" % (
      self.server_host, self.server_port, str(self.server_debug),
      self.db_host, self.db_port, self.db_name, self.db_user, self.db_password)

  def fromEnv(self):
    host = os.getenv('SERVER_HOST')
    if host is not None:
      self.server_host = host

    port = os.getenv('SERVER_PORT')
    if port is not None and isinstance(port, int):
      self.server_port = port

    debug = os.getenv('SERVER_DEBUG') == 'true'
    if debug:
      self.server_debug = debug

    self.db_host = os.getenv('DB_HOST')
    self.db_port = os.getenv('DB_PORT')
    self.db_name = os.getenv('DB_NAME')
    self.db_user = os.getenv('DB_USER')
    self.db_password = os.getenv('DB_PASSWORD')

    return self

  def isDatabaseConfigured(self) -> bool:
    return (self.db_host is not None and
      self.db_port is not None and
      self.db_name is not None and
      self.db_user is not None and
      self.db_password is not None)