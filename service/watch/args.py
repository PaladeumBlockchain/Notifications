from webargs import fields, validate

watch_args = {
    "device": fields.Str(required=True, validate=validate.Length(min=4, max=40)),
    "addresses": fields.List(fields.Str(), required=True)
}
