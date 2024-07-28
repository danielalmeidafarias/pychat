from marshmallow import Schema, fields


class SignInSchema(Schema):
    email = fields.Str()
    password = fields.Str()
