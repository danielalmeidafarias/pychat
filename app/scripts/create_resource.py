import os
import sys

args = sys.argv
name = args[1]

# Checking parameters size
# It have one default parameter
if len(args) > 2:
    print('You need to pass only one parameter')

else:
    folder_path = f"app/{name}"

    # Creating a default resource file
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

        # Creating and writing on new files
        main_file = open(f"{folder_path}/{name}.py", 'w')
        main_file.writelines([
            "from flask import request\n"
            "from flask_restx import Resource, Namespace\n"
            "from app.db import db\n"
            "from marshmallow.exceptions import ValidationError\n"
            f"from .model import {name.capitalize()}Model\n"
            f"from .schemas import Get{name.capitalize()}Schema, Create{name.capitalize()}Schema, Update{name.capitalize()}Schema, Delete{name.capitalize()}Schema\n"
            f"from .docs.response_models import {name.capitalize()}ResponseModels\n"
            f"from .docs.request_models import {name.capitalize()}RequestModels\n"
            "from app.common.docs.response_models import CommonResponseModels\n"
            "\n"
            "\n"
            f"{name}_namespace = Namespace('{name}', '{name.capitalize()} Route')\n"
            f"requests = {name.capitalize()}RequestModels({name}_namespace)\n"
            f"responses = {name.capitalize()}ResponseModels({name}_namespace)\n"
            f"common_responses = CommonResponseModels({name}_namespace)\n"
            "\n"
            "\n"
            f"@{name}_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')\n"
            f"@{name}_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')\n"
            f"@{name}_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')\n"
            f"@{name}_namespace.route('')\n"
            f"class {name.capitalize()}Resource(Resource):\n"
            "    def get(self):\n"
            "        pass\n"
            "\n"
            "    def post(self):\n"
            "        data = request.get_json()\n"
            f"        schema = Create{name.capitalize()}Schema()\n"
            "        validated_data = schema.dump(data)\n"
            "\n"
            "        try:\n"
            "            schema.load(validated_data)\n"
            "        except ValidationError as err:\n"
            "            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400\n"
            "        pass\n"
            "\n"
            "\n"
            f"@{name}_namespace.route('/<id>')\n"
            f"class Unique{name.capitalize()}Resource(Resource):\n"
            "    def put(self):\n"
            "        data = request.get_json()\n"
            f"        schema = Update{name.capitalize()}Schema()\n"
            "        validated_data = schema.dump(data)\n"
            "\n"
            "        try:\n"
            "            schema.load(validated_data)\n"
            "        except ValidationError as err:\n"
            "            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400\n"
            "        pass\n"
            "\n"
            "    def delete(self):\n"
            "        pass\n"
        ])
        main_file.close()

        model_file = open(f"{folder_path}/model.py", 'w')
        model_file.writelines([
            "import uuid\n"
            "from sqlalchemy.orm import Mapped, mapped_column\n"
            "from app.db import db\n"
            "\n"
            "\n"
            f"class {name.capitalize()}Model(db.Model):\n"
            "    def __init__(self):\n"
            "       pass\n"
            "\n"
            "    __table_args__ = {'extend_existing': True}\n"
            "\n"
            "    __tablename__ = 'user'\n"
            "\n"
            "    id: Mapped[str] = mapped_column(primary_key=True)\n"
             "\n"
            "    def __repr__(self) -> str:\n"
            '        return f"{{id:{self.id}}}"\n'
            "\n"
        ])
        model_file.close()

        repository_file = open(f"{folder_path}/repository.py", 'w')
        repository_file.writelines([
            "from flask_sqlalchemy import SQLAlchemy\n"
            "\n"
            "\n"
            f"class {name.capitalize()}Repository():\n"
            "    def __init__(self, db: SQLAlchemy):\n"
            "        self.db = db\n"
            "\n"
            f"    def create(self, {name}_id: str):\n"
            "        pass\n"
            "\n"
            f"    def get(self, {name}_id: str):\n"
            "        pass\n"
            "\n"
            "    def get_all(self):\n"
            "        pass\n"
            "\n"
            f"    def update(self, {name}_id: str):\n"
            "        pass\n"
            "\n"
            f"    def delete(self, {name}_id: str):\n"
            "        pass\n"
            "\n"
        ])

        schemas_file = open(f"{folder_path}/schemas.py", 'w')
        schemas_file.writelines([
            "from marshmallow import Schema, fields\n"
            "\n"
            "\n"
            f"class Create{name.capitalize()}Schema(Schema):\n"
            "    pass"
            "\n"
            "\n"
            f"class Get{name.capitalize()}Schema(Schema):\n"
            "    pass"
            "\n"
            "\n"
            f"class Update{name.capitalize()}Schema(Schema):\n"
            "    pass"
            "\n"
            "\n"
            f"class Delete{name.capitalize()}Schema(Schema):\n"
            "    pass"
            "\n"
        ])
        schemas_file.close()

        os.mkdir(folder_path + '/docs')
        request_models_file = open(f"{folder_path}/docs/request_models.py", 'w')
        request_models_file.writelines([
            "from flask_restx import fields, Namespace\n"
            "\n"
            "\n"
            f"class {name.capitalize()}RequestModels:\n"
            "    def __init__(self, nm: Namespace):\n"
            f"        self.create_{name} = nm.model('Create {name}', {{}})\n"
            f"        self.get_{name} = nm.model('Get {name}', {{}})\n"
            f"        self.update_{name} = nm.model('Update {name}', {{}})\n"
            f"        self.delete_{name} = nm.model('Delete {name}', {{}})\n"

        ])
        request_models_file.close()

        response_models_file = open(f"{folder_path}/docs/response_models.py", 'w')
        response_models_file.writelines([
            "from flask_restx import fields, Namespace\n"
            "\n"
            "\n"
            f"class {name.capitalize()}ResponseModels:\n"
            "    def __init__(self, nm: Namespace):\n"
            "\n"
            f"        self.post_201 = nm.model(name='{name}_post_201_model', model={{\n"
            "            'message': fields.Raw(''),\n"
            "        })\n"
            "\n"
            f"        self.post_409 = nm.model(name='{name}_post_409_model', model={{\n"
            "            'message': fields.Raw('')\n"
            "        })\n"
            "\n"
            f"        self.get_200 = nm.model(name='{name}_get_200', model={{\n"
            "            'message': fields.Raw('')\n"
            "        })\n"
            "\n"
        ])
        response_models_file.close()

        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")
