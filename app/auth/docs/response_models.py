from flask_restx import fields, Namespace


class AuthResponseModels:
    def __init__(self, nm: Namespace):
        self.post_200 = nm.model(name="auth_post_200_model", model={
                "access_token": fields.Raw("jwt token")
            }
        )
