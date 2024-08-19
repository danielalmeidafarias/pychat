from marshmallow import Schema, fields
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


def test_user_already_exists(client, user):
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


def test_created_user_in_db(client, user, user_repository):
    db_user = user_repository.get_one(user['id'])

    assert db_user['id'] == user['id'] and \
           db_user['email'] == user['email'] and \
           bcrypt.checkpw(str.encode("Daniel@123"), db_user['password'])


def test_get_all_users(client, user, access_token):
    response = client.get('/user', headers={
        "Authorization": access_token
    })

    assert response.json['users'] == [{'id': f"{user['id']}", 'name': 'Daniel'}]


def test_get_one_user(client, access_token, user):
    response = client.get('/user', headers={
        "Authorization": access_token
    }, query_string={"user_id": user['id']})

    # assert response.json['user']['id'] == created_user['id']
    assert response.status_code == 200


