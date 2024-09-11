from marshmallow import Schema, fields


class CreateMessageSchema(Schema):
    content = fields.String(required=True)
    chat_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)

class GetMessageSchema(Schema):
    message_id = fields.UUID(required=False, allow_none=True)
    chat_id = fields.UUID(required=False, allow_none=True)
    user_id = fields.UUID(required=False, allow_none=True)

class UpdateMessageSchema(Schema):
    content = fields.String(required=True)
