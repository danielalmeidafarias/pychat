from flask_restx import fields, Namespace


class CommonResponseModels:
    def __init__(self, nm: Namespace):
        data_validation_post_400_error = nm.model(name="data_validation_400_error", model={
            "field": fields.List(fields.String)
        })

        self.data_validation_error = nm.model(name="data_validation_400", model={
            "message": fields.Raw("Data Validation Error"),
            "errors": fields.Nested(data_validation_post_400_error)
        })

        self.unauthorized = nm.model(name="unauthorized", model={
            "message": fields.Raw("Unauthorized!")
        })
