from webargs.flaskparser import use_args
from ..services import AddressService
from ..services import DeviceService
from .args import watch_args
from flask import Blueprint
from ..abort import abort
from pony import orm
from .. import utils

blueprint = Blueprint("watch", __name__)

@blueprint.route("/watch", methods=["POST"])
@use_args(watch_args, location="json")
@orm.db_session
def set(args):
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
        "device": device.device_id
    }

    return result
