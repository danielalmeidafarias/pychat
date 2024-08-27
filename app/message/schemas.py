from marshmallow import Schema, fields


class CreateMessageSchema(Schema):
    content = fields.String()
    chat_id = fields.UUID()

class GetMessageSchema(Schema):
    pass

class UpdateMessageSchema(Schema):
    pass

class DeleteMessageSchema(Schema):
    pass
