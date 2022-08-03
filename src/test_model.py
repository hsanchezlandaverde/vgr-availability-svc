from datetime import datetime
from models import Availability

def testStr():
  availability = Availability(1, "Available", datetime(2022, 8, 2, 12, 30, 0), datetime(2022, 8, 2, 12, 30, 0))
  expected = "{ id: 1, name: Available, created_at: 2022-08-02 12:30:00, updated_at: 2022-08-02 12:30:00 }"
  actual = str(availability)
  assert expected == actual

def testDict():
  availability = Availability(1, "Available", datetime(2022, 8, 2, 12, 30, 0), datetime(2022, 8, 2, 12, 30, 0))
  expected = {
    "id": 1,
    "name": "Available",
    "created_at": "2022-08-02 12:30:00",
    "updated_at": "2022-08-02 12:30:00"
  }
  actual = availability.dict()
  assert expected == actual
