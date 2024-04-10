from .base import db
from pony import orm

class Address(db.Entity):
    raw_address = orm.Required(str, index=True)
    notifications = orm.Set("Notification")
    devices = orm.Set("Device")
