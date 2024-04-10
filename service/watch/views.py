from service.services import SwapNotificationService
from service.services import AddressService
from service.services import DeviceService
from webargs.flaskparser import use_args
from .args import watch_args, swap_args
from service.abort import abort
from flask import Blueprint
from service import utils
from pony import orm
import config


blueprint = Blueprint("watch", __name__)


@blueprint.route("/watch", methods=["POST"])
@use_args(watch_args, location="json")
@orm.db_session
def add_watch(args):
    result = {"error": None, "data": {}}

    addresses = args["addresses"]
    device_id = args["device"]

    if not utils.validate_player_id(device_id):
        return abort("watch", "bad-device-id")

    for address in addresses:
        if not utils.validate_address(address):
            return abort("watch", "invalid-address")

    if not (device := DeviceService.get_by_id(device_id)):
        device = DeviceService.create(device_id)

    device.addresses.clear()

    for raw_address in addresses:
        if not (address := AddressService.get_by_raw_address(raw_address)):
            address = AddressService.create(raw_address)

        device.addresses.add(address)

    result["data"] = {
        "addresses": len(device.addresses),
        "device": device.device_id,
    }

    return result


@blueprint.route("/swap", methods=["POST"])
@use_args(swap_args, location="json")
@orm.db_session
def add_swap(args):
    result = {"error": None, "data": {}}

    if args["auth"] != config.auth:
        return abort("swap", "bad-auth")

    receive_currency = args["receive_currency"]
    receive_amount = args["receive_amount"]
    send_currency = args["send_currency"]
    send_amount = args["send_amount"]
    raw_address = args["address"]
    order_id = args["order_id"]

    if not (address := AddressService.get_by_raw_address(raw_address)):
        return abort("swap", "untracked-address")

    SwapNotificationService.create(
        receive_amount=utils.float_to_Decimal(receive_amount),
        send_amount=utils.float_to_Decimal(send_amount),
        receive_currency=receive_currency,
        send_currency=send_currency,
        order_id=order_id,
        address=address,
    )

    result["data"] = {
        "receive_currency": receive_currency,
        "receive_amount": receive_amount,
        "send_currency": send_currency,
        "send_amount": send_amount,
        "raw_address": raw_address,
        "order_id": order_id,
    }

    return result
