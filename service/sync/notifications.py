from config import onesignal_authorization, onesignal_app_id
from service.services import SwapNotificationService
from service.services import NotificationService
from pony import orm
import requests


def send_notification(device_id, message):
    headers = {
        "Accept": "application/json",
        "Authorization": onesignal_authorization,
    }

    json_data = {
        "include_player_ids": [
            device_id,
        ],
        "contents": {
            "en": message,
        },
        "app_id": onesignal_app_id,
    }

    response = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=headers,
        json=json_data,
    )

    if response.status_code != 200:
        print(f"Couldn't send notification: {response.text}")


@orm.db_session
def send_notifications():
    for notification in NotificationService.get_unprocessed():
        address = notification.address

        display_amount = (
            "{:,.4f}".format(float(notification.amount)).rstrip("0").rstrip(".")
        )

        message = f"You received {display_amount} {notification.ticker}"

        for device in address.devices:
            send_notification(device.device_id, message)

        notification.processed = True


@orm.db_session
def send_swap_notifications():
    for notification in SwapNotificationService.get_unprocessed():
        address = notification.address

        display_receive_amount = (
            "{:,.4f}".format(float(notification.receive_amount))
            .rstrip("0")
            .rstrip(".")
        )

        display_send_amount = (
            "{:,.4f}".format(float(notification.send_amount))
            .rstrip("0")
            .rstrip(".")
        )

        message = f"You received request to swap {display_receive_amount} {notification.receive_currency} for {display_send_amount} {notification.send_currency}"

        for device in address.devices:
            send_notification(device.device_id, message)

        notification.processed = True
