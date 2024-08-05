from flask_restx import fields, Namespace
from ...common.docs.response_models import CommonResponseModels


class AuthResponseModels:
    def __init__(self, nm: Namespace):
        common_responses = CommonResponseModels(nm)

        self.post_400 = common_responses.data_validation_error

        self.post_401 = common_responses.unauthorized

        self.post_200 = nm.model(name="auth_post_200_model", model={
                "access_token": fields.Raw("jwt token")
            }
        )

        self.post_404 = common_responses.no_user_found
