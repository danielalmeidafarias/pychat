from flask_restx import fields, Namespace


def get_responses(nm: Namespace):
    create_user_model = nm.model('Create User', {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    })

    return create_user_model
