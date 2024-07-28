from flask_restx import fields, Namespace
from ...common.docs.response_models import common_response_models


def response_models(nm: Namespace):
    common_responses = common_response_models(nm)
    responses = {}

    responses['post_400'] = common_responses["data_validation_error"]

    responses['post_401'] = common_responses["unauthorized"]

    responses["post_200"] = nm.model(name="auth_post_200_model", model={
            "access_token": fields.Raw("jwt token")
        }
    )

    responses["post_404"] = nm.model(name="auth_post_404_model", model={
        "message": fields.Raw("No user with this credentials was found, please check the email")
    })

    return responses
