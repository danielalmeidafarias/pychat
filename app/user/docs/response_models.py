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

        self.get_400 = common_responses.no_user_found

        user_response = nm.model(name="user_model", model={
            "id": fields.String,
            "name": fields.String
        })

        self.get_all_200 = nm.model(name="user_get_all_200", model={
            "users": fields.List(fields.Nested(user_response))
        })

        self.get_one_200 = nm.model(name="user_get_one_200", model={
            "user": fields.Nested(user_response)
        })

        self.internal_error = common_responses.internal_error

