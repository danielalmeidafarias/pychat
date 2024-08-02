from flask_restx import fields, Namespace


class AuthRequestModels:
    def __init__(self, nm: Namespace):
        self.signin = nm.model(name="Signin model", model={
            "email": fields.String,
            "password": fields.String
        })
