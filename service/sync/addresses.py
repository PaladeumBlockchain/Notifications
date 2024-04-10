from ..services import AddressService, NotificationService
from ..utils import float_to_Decimal
from ..models import Settings
from .. import utils
from pony import orm


def get_current_height():
    return utils.make_request("getblockcount")["result"]


def get_height(height: int):
    return utils.make_request("getblockhash", [height])["result"]


def get_block_hash(height: int):
    return utils.make_request("getblockhash", [height])["result"]


def get_block(blockhash: str):
    return utils.make_request("getblock", [blockhash])["result"]


def get_transaction(txid: str):
    data = utils.make_request("getrawtransaction", [txid, True])

    for index, vin in enumerate(data["result"]["vin"]):
        if "txid" in vin:
            vin_data = utils.make_request(
                "getrawtransaction", [vin["txid"], True]
            )
            if vin_data["error"] is None:
                data["result"]["vin"][index]["scriptPubKey"] = vin_data[
                    "result"
                ]["vout"][vin["vout"]]["scriptPubKey"]

    return data["result"]


@orm.db_session
def check_addresses():
    # Get latest chain height
    latest_height = get_current_height()

    # Get settings object
    if not (settings := Settings.select().for_update().first()):
        # Init settings in case of first run
        settings = Settings(height=latest_height)

    # Process blocks
    while settings.height <= latest_height:
        print(f"Processing block {settings.height}")

        block_data = get_block(get_height(settings.height))

        # Process transactions
        for txid in block_data["tx"]:
            tx = get_transaction(txid)
            pairs = []

            for vin in tx["vin"]:
                if "txid" not in vin:
                    continue

                vin_data = get_transaction(vin["txid"])

                ticker = "PLB"
                raw_address = ""

                vout = vin_data["vout"][vin["vout"]]

                if "scriptPubKey" not in vout:
                    continue

                if "addresses" not in vout["scriptPubKey"]:
                    continue

                if "token" in vout["scriptPubKey"]:
                    ticker = vout["scriptPubKey"]["token"]["name"]

                raw_address = vout["scriptPubKey"]["addresses"][0]

                pairs.append((raw_address, ticker))

            for vout in tx["vout"]:
                ticker = "PLB"
                raw_address = ""
                amount = 0

                if "scriptPubKey" not in vout:
                    continue

                if "addresses" not in vout["scriptPubKey"]:
                    continue

                if "token" in vout["scriptPubKey"]:
                    ticker = vout["scriptPubKey"]["token"]["name"]
                    amount = vout["scriptPubKey"]["token"]["amount"]
                else:
                    amount = vout["value"]

                raw_address = vout["scriptPubKey"]["addresses"][0]

                if not (
                    address := AddressService.get_by_raw_address(raw_address)
                ):
                    continue

                if len(address.devices) <= 0:
                    continue

                if (raw_address, ticker) in pairs:
                    continue

                print(f"Added notification to for {raw_address}")

                NotificationService.create(
                    amount=float_to_Decimal(amount),
                    address=address,
                    ticker=ticker,
                    txid=txid,
                )

        settings.height += 1
