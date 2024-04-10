from webargs import fields, validate

watch_args = {
    "device": fields.Str(
        required=True, validate=validate.Length(min=4, max=40)
    ),
    "addresses": fields.List(fields.Str(), required=True),
}

swap_args = {
    "receive_currency": fields.Str(required=True),
    "receive_amount": fields.Float(required=True),
    "send_currency": fields.Str(required=True),
    "send_amount": fields.Float(required=True),
    "order_id": fields.Str(required=True),
    "address": fields.Str(required=True),
    "auth": fields.Str(required=True),
}
