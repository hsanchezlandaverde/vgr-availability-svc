import os

APP_NAME = "vgr-availability-svc"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8092

class Configuration:

  def __init__(self):
    self.app_name = APP_NAME
    self.host = DEFAULT_HOST
    self.port = DEFAULT_PORT
    self.debug = False

  def __str__(self):
    return "{ debug: %s, port: %d }" % (str(self.debug), self.port)

  def fromEnv(self):
    host = os.getenv('HOST')
    if host is not None:
      self.host = host

    port = os.getenv('PORT')
    if port is not None and isinstance(port, int):
      self.port = port

    debug = os.getenv('DEBUG_ENABLED') == 'true'
    if debug:
      self.debug = debug

    return self
