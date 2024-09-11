from marshmallow import Schema, fields, ValidationError


class ValidStatus(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if data['status'] != 'accepted' and data['status'] != 'refused':
            raise ValidationError("status must be 'accepted' or 'refused")


class CreateFriendshipRequestSchema(Schema):
    sender_id = fields.UUID(required=True)
    receiver_id = fields.UUID(required=True)


class GetFriendshipRequestSchema(Schema):
    id = fields.UUID(required=False, allow_none=True)
    sender_id = fields.UUID(required=False, allow_none=True)
    receiver_id = fields.UUID(required=False, allow_none=True)


class UpdateFriendshipRequestSchema(Schema):
    status = ValidStatus(required=True)
