from marshmallow import Schema, fields


class CreateChatMembersSchema(Schema):
    user_id = fields.UUID(required=True)
    chat_id = fields.UUID(required=True)
    role = fields.Str(required=False, allow_none=True)


class GetChatMembersSchema(Schema):
    user_id = fields.UUID(required=False, allow_none=True)
    chat_id = fields.UUID(required=False, allow_none=True)


class UpdateChatMembersSchema(Schema):
    role = fields.Str(required=False, allow_none=True)
