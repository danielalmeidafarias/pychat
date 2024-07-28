from flask_restx import fields, Namespace


def common_response_models(nm: Namespace):
    responses = {}

    data_validation_post_400_error = nm.model(name="data_validation_400_error", model={
        "field": fields.List(fields.String)
    })

    responses["data_validation_error"] = nm.model(name="data_validation_400", model={
        "message": fields.Raw("Data Validation Error"),
        "errors": fields.Nested(data_validation_post_400_error)
    })

    responses["unauthorized"] = nm.model(name="unauthorized", model={
        "message": fields.Raw("Unauthorized!")
    })

    return responses
