from flask_restx import fields, Namespace


def get_responses(nm: Namespace):
    signin_model = nm.model(name="Signin model", model={
        "email": fields.String,
        "password": fields.String
    })

    return signin_model
