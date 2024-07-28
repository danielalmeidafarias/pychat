from flask_restx import fields, Namespace


def request_models(nm: Namespace):
    requests = {}

    requests["signin"] = nm.model(name="Signin model", model={
        "email": fields.String,
        "password": fields.String
    })

    return requests
