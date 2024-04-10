errors = {
    "watch": {
        "bad-device-id": "Invalid device id",
        "invalid-address": "Invalid address"
    }
}

# Return error message
def abort(scope, message):
    code = scope.replace("-", "_") + "_" + message.replace("-", "_")

    try:
        error_message = errors[scope][message]
    except Exception:
        error_message = "Unknown error"

    return {
        "error": {
            "message": error_message,
            "code": code
        },
        "data": {}
    }
