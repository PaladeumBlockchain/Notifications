from .base import db
from pony import orm


class Address(db.Entity):
    raw_address = orm.Required(str, index=True)
    swap_notifications = orm.Set("SwapNotification")
    notifications = orm.Set("Notification")
    devices = orm.Set("Device")
