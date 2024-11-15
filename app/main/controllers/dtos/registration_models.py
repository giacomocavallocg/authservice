from marshmallow import Schema, fields, EXCLUDE

class RegistrationDto(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    age = fields.Integer(required=False, load_default = None)
    use_2fv = fields.Bool(required=False, data_key = "use2fa", load_default = False)

    class Meta:
        unknown = EXCLUDE

class LoginDto(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class TwoFactorDto(Schema):
    request_id = fields.String(required=True)
    otp = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE

