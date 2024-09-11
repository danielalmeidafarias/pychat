from marshmallow import Schema, fields


class CreateChatSchema(Schema):
    name: str = fields.Str(required=True)


class GetChatSchema(Schema):
    name: str = fields.Str(required=False, allow_none=True)
    chat_id: str = fields.UUID(required=False, allow_none=True)


class UpdateChatSchema(Schema):
    name: str = fields.Str(required=False, allow_none=True)
