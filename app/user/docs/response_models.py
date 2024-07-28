from flask_restx import fields, Namespace
from ...common.docs.response_models import common_response_models


def response_models(nm: Namespace):
    common_responses = common_response_models(nm)
    responses = {}

    responses["post_400"] = common_responses["data_validation_error"]

    responses["post_201"] = nm.model(name="user_post_201_model", model={
        "message": fields.Raw("User Created with success!"),
        "id": fields.Raw('user_id'),
        "email": fields.String,
        "name": fields.String
    })

    responses["post_409"] = nm.model(name="user_post_409_model", model={
        "message": fields.Raw("There is already a user with this credentials")
    })

    return responses
