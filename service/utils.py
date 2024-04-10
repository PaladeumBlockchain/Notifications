from decimal import Decimal
import requests
import config
import json


def float_to_Decimal(num):
    return Decimal(str(num))


def dead_response(message="Invalid Request", rid="plb-notifications"):
    return {"error": {"code": 404, "message": message}, "id": rid}


def response(result, error=None, rid="plb-notifications", pagination=None):
    result = {"error": error, "id": rid, "result": result}

    if pagination:
        result["pagination"] = pagination

    return result


def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps(
        {"id": "plb-notifications", "method": method, "params": params}
    )

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()


def validate_player_id(player_id):
    headers = {
        "Accept": "text/plain",
        "Authorization": f"Basic {config.onesignal_authorization}",
        "Content-Type": "application/json; charset=utf-8",
    }

    params = {"app_id": config.onesignal_app_id}

    response = requests.get(
        f"https://onesignal.com/api/v1/players/{player_id}",
        params=params,
        headers=headers,
    )

    return "errors" not in response.json()


def validate_address(address):
    data = make_request("validateaddress", [address])

    if data["error"]:
        return False

    return data["result"]["isvalid"]
