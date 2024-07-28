from flask_restx import fields, Namespace


def request_models(nm: Namespace):
    requests = {}

    requests['create_user'] = nm.model('Create User', {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    })

    return requests
