from marshmallow import Schema, fields


class CreateChatSchema(Schema):
    content = fields.String()
    user_id = fields.String()
    chat_id = fields.String()

class GetChatSchema(Schema):
    pass

class UpdateChatSchema(Schema):
    pass

class DeleteChatSchema(Schema):
    pass
