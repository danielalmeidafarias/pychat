from marshmallow import Schema, fields, ValidationError
from password_strength import PasswordPolicy

password_policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=3,
    special=1,
)


class StrongPassword(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        password: str = data['password']
        strong_password_errors = password_policy.test(password)

        if len(strong_password_errors) > 0:
            raise ValidationError(
                "Password must have at least 8 characters, "
                "including 3 numbers, "
                "1 special character "
                "and 1 uppercase letter"
                )


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = StrongPassword(required=True)


class UpdateUserSchema(Schema):
    def __init__(self):
        super().__init__()
        self.strict = True

    name = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    password = StrongPassword(allow_none=True)
