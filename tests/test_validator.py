from app import validation_utils

valid = validation_utils.Validator()

def testStr():
  assert valid.__str__() == "Validator::Std"

def testAvailability_GivenValidObj_ReturnFalse():
  availability = { "id": 1, "name": "Available" }
  assert valid.availability(availability) == True

def testAvailability_GivenEmptyObj_ReturnFalse():
  availability = {}
  assert valid.availability(availability) == False
  
def testName_GivenStringGreaterMinLen_ReturnTrue():
  name = "foobar"
  assert valid.name(name) == True

def testName_GivenStringBelowMinLen_ReturnFalse():
  name = "foo"
  assert valid.name(name) == False

def testId_GivenZeroId_ReturnFalse():
  id = 0
  assert valid.id(id) == False

def testId_GivenNegativeId_ReturnFalse():
  id = -254
  assert valid.id(id) == False

def testId_GivenValidId_ReturnTrue():
  id = 16
  assert valid.id(id) == True