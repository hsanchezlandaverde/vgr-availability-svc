import configuration

def testInit():
  config = configuration.Configuration()
  assert config.server_host == configuration.DEFAULT_HOST
  assert config.server_port == configuration.DEFAULT_PORT
  assert config.server_debug == False
  assert config.db_host == None
  assert config.db_port == None
  assert config.db_name == None
  assert config.db_user == None
  assert config.db_password == None

def testStr():
  config = configuration.Configuration()
  config.server_host = "0.0.0.0"
  config.server_port = 8092
  config.server_debug = True
  config.db_host = "127.0.0.1"
  config.db_port = 5432
  config.db_name = "vgr-availabilities"
  config.db_user = "vgr"
  config.db_password = "Vgr2022!"
  expected = "{ server_host: 0.0.0.0, server_port: 8092, server_debug: True, db_host: 127.0.0.1, db_port: 5432, db_name: vgr-availabilities, db_user: vgr, db_password: Vgr2022! }"
  actual = str(config)
  assert expected == actual

def testIsDatabaseConfigured_WhenNotConfigured_ExpectFalse():
  config = configuration.Configuration()
  assert False == config.isDatabaseConfigured()

def testIsDatabaseConfigured_WhenPartialConfigured_ExpectFalse():
  config = configuration.Configuration()
  config.db_host = "127.0.0.1"
  config.db_port = 5432
  config.db_user = "vgr"
  config.db_password = "Vgr2022!"
  assert False == config.isDatabaseConfigured()

def testIsDatabaseConfigured_WhenConfigured_ExpectTrue():
  config = configuration.Configuration()
  config.db_host = "127.0.0.1"
  config.db_port = 5432
  config.db_name = "vgr-availabilities"
  config.db_user = "vgr"
  config.db_password = "Vgr2022!"
  assert True == config.isDatabaseConfigured()