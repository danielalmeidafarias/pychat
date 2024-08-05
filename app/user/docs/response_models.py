from flask_restx import fields, Namespace
from ...common.docs.response_models import CommonResponseModels


class UserResponseModels:
    def __init__(self, nm: Namespace):
        common_responses = CommonResponseModels(nm)

        self.post_400 = common_responses.data_validation_error

        self.post_201 = nm.model(name="user_post_201_model", model={
            "message": fields.Raw("User Created with success!"),
            "id": fields.Raw('user_id'),
            "email": fields.String,
            "name": fields.String
        })

        self.post_409 = nm.model(name="user_post_409_model", model={
            "message": fields.Raw("There is already a user with this credentials!")
        })
