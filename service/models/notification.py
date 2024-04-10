from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm

class Notification(db.Entity):
    created = orm.Optional(datetime, default=datetime.utcnow)
    amount = orm.Required(Decimal, precision=20, scale=8)
    processed = orm.Required(bool, default=False)
    address = orm.Required("Address")
    ticker = orm.Required(str)
    txid = orm.Required(str)
