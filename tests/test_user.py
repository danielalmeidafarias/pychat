from marshmallow import Schema, fields
from app.db import db
from app.user.model import UserModel
import bcrypt


def test_create_user(client):
    response = client.post('/user', json={
        "email": "daniel@email.com",
        "name": "Daniel",
        "password": "Daniel@123"
    })

    response_data = response.json

    class ResponseSchema(Schema):
        message = fields.Str()
        id = fields.UUID()
        name = fields.Str()
        email = fields.Email()

    response_schema = ResponseSchema()

    response_schema.dump(response_data)

    assert response.status_code == 201


def test_user_already_exists(client, created_user):
    response = client.post('/user', json={
        "email": "daniel@email.com",
        "name": "Daniel2",
        "password": "Daniel@13123123"
    })

    assert response.status_code == 409 and \
           response.json['message'] == "There is already a user with this credentials!"


def test_bad_email_error(client):
    response = client.post('/user', json={
        "email": "bad_email.com",
        "name": "Daniel2",
        "password": "Daniel@13123123"
    })

    assert response.status_code == 400 and \
           response.json['message'] == "Data Validation Error!"


def test_weak_password_error(client):
    response = client.post('/user', json={
        "email": "daniel@email.com",
        "name": "Daniel2",
        "password": "daniel"
    })

    assert response.status_code == 400 and \
           response.json['message'] == "Data Validation Error!"


def test_created_user_in_db(client, created_user):
    user_id = created_user['id']

    user = db.session.execute(db.select(UserModel).where(UserModel.id == user_id)).scalar_one()

    assert user.id == user_id and \
           user.email == user.email and \
           bcrypt.checkpw(str.encode("Daniel@123"), user.password)


def test_get_all_users(client, access_token):
    response = client.get('/user', headers={
        "Authorization": access_token
    })

    assert response.json == {'users': []}


def test_get_one_user(client, access_token, created_user):
    response = client.get('/user', headers={
        "Authorization": access_token
    }, query_string={"user_id": created_user['id']})

    assert response.json['user']['id'] == created_user['id']

