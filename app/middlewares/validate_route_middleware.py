from flask import request, redirect
from functools import wraps
from marshmallow import ValidationError, Schema as SchemaBaseClass


class ValidateRouteMiddleware:
    def __init__(self, schema: type[SchemaBaseClass]):
        self.Schema = schema

    def middleware(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.form.to_dict()
            schema = self.Schema()
            validated_data = schema.dump(data)

            try:
                schema.load(validated_data)
                return func(*args, **kwargs)
            except ValidationError as err:
                print('middleware')
                return {"message": "Data Validation Error!", "errors": err.messages}, 400

        return wrapper

