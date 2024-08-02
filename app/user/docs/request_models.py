from flask_restx import fields, Namespace


class UserRequestModels:
    def __init__(self, nm: Namespace):
        self.crate_user = nm.model('Create User', {
            "name": fields.String(required=True),
            "email": fields.String(required=True),
            "password": fields.String(required=True)
        })
