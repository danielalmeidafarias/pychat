from marshmallow import Schema, fields


class CreateFriendshipRequestSchema(Schema):
    recipient_id = fields.Str()

class GetFriendshipRequestSchema(Schema):
    pass

class UpdateFriendshipRequestSchema(Schema):
    pass

class DeleteFriendshipRequestSchema(Schema):
    pass
