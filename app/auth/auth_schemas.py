from marshmallow import Schema, fields


class SignInSchema(Schema):
    email = fields.Email()
    password = fields.Str()
