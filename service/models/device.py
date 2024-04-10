from .base import db
from pony import orm

class Device(db.Entity):
    device_id = orm.Required(str, index=True)
    addresses = orm.Set("Address")
