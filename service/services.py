from .models import SwapNotification
from .models import Notification
from .models import Address
from .models import Device


class DeviceService(object):
    @classmethod
    def get_by_id(cls, device_id):
        return Device.get(device_id=device_id)

    @classmethod
    def create(cls, device_id):
        return Device(device_id=device_id)


class AddressService(object):
    @classmethod
    def get_by_raw_address(cls, raw_address):
        return Address.get(raw_address=raw_address)

    @classmethod
    def create(cls, raw_address):
        return Address(raw_address=raw_address)


class NotificationService(object):
    @classmethod
    def get_unprocessed(cls):
        return Notification.select(processed=False)

    @classmethod
    def create(cls, amount, address, ticker, txid):
        return Notification(
            amount=amount, address=address, ticker=ticker, txid=txid
        )


class SwapNotificationService(object):
    @classmethod
    def get_unprocessed(cls):
        return SwapNotification.select(processed=False)

    @classmethod
    def create(
        cls,
        receive_amount,
        receive_currency,
        send_amount,
        send_currency,
        address,
        order_id,
    ):
        return SwapNotification(
            receive_amount=receive_amount,
            receive_currency=receive_currency,
            send_amount=send_amount,
            send_currency=send_currency,
            address=address,
            order_id=order_id,
        )
