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
                "Password must have at least eight characters, "
                "including three numbers, "
                "one special character "
                "and one uppercase letter"
                )


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = StrongPassword(required=True)


class UpdateUserSchema(Schema):
    name = fields.Str(required=False, allow_none=True)
    email = fields.Email(required=False, allow_none=True)
    password = fields.Str(required=True, allow_none=True)
    new_password = StrongPassword(required=False, allow_none=True)


class GetUserSchema(Schema):
    user_id = fields.Integer(required=False, allow_none=True)


class DeleteUserSchema(Schema):
    password = fields.Str(required=False, allow_none=False)
