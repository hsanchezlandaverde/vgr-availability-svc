DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class Availability:

  def __init__(self, id, name, created_at, updated_at):
    self.id = id
    self.name = name
    self.created_at = created_at
    self.updated_at = updated_at

  def __str__(self):
    return """{ id: %d, name: %s, created_at: %s, updated_at: %s }""" % (
      self.id, self.name, self.created_at, self.updated_at)

  def dict(self) -> dict:
    return {
      "id": self.id,
      "name": self.name,
      "created_at": self.created_at.strftime(DATETIME_FORMAT),
      "updated_at": self.updated_at.strftime(DATETIME_FORMAT),
    }