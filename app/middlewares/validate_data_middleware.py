from flask import request, redirect
from functools import wraps
from marshmallow import ValidationError, Schema as SchemaBaseClass


class ValidateDataMiddleware:
    def __init__(self, schema: type[SchemaBaseClass]):
        self.Schema = schema

    def middleware(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = self.Schema()
            if request.method == "GET":
                data = request.args.to_dict()
            elif request.method == "POST" or request.method == "PUT":
                if request.mimetype == 'multipart/form-data':
                    data = request.form.to_dict()
                else:
                    data = request.get_json()

            validated_data = schema.dump(data)
            try:
                schema.load(validated_data)
                return func(*args, **kwargs)
            except ValidationError as err:
                return {"message": "Data Validation Error!", "errors": err.messages}, 400
        return wrapper

