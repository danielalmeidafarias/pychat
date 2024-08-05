from flask_restx import fields, Namespace


class CommonResponseModels:
    def __init__(self, nm: Namespace):
        data_validation_post_400_error = nm.model(name="data_validation_400_error", model={
            "field": fields.List(fields.String)
        })

        self.data_validation_error = nm.model(name="data_validation_400", model={
            "message": fields.Raw("Data Validation Error!"),
            "errors": fields.Nested(data_validation_post_400_error)
        })

        self.unauthorized = nm.model(name="unauthorized", model={
            "message": fields.Raw("Unauthorized!")
        })

        self.no_user_found = nm.model(name="auth_post_404_model", model={
            "message": fields.Raw("No user with this credentials was found, please check the email")
        })

        self.internal_error = nm.model('internal_error', model={
            "message": fields.Raw("I'm sorry, something went wrong. Try again later")
        })
