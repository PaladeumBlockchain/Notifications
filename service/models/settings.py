from .base import db
from pony import orm

class Settings(db.Entity):
    height = orm.Required(int)
