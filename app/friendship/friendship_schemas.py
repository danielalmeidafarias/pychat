from marshmallow import Schema, fields


class GetFriendshipSchema(Schema):
    user_id = fields.Str(required=False, allow_none=True)
