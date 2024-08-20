from marshmallow import Schema, fields, ValidationError


class CreateFriendshipRequestSchema(Schema):
    sender_id = fields.UUID()
    receiver_id = fields.UUID()


class GetFriendshipRequestSchema(Schema):
    pass


class ValidStatus(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if data['status'] != 'accepted' and data['status'] != 'refused':
            raise ValidationError("status must be 'accepted' or 'refused")


class UpdateFriendshipRequestSchema(Schema):
    status = ValidStatus(required=True)


class DeleteFriendshipRequestSchema(Schema):
    pass
