from app.db import db


def test_send_friendship_request(client, access_token, user, user2, user_repository):
    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': user2['id']
    })

    db_user = user_repository.get(user['id'])
    db_user2 = user_repository.get(user2['id'])

    assert db_user['sent_friendship_request'] == db_user2['id'] and \
        db_user2['friendship_request'] == db_user['id'] and \
        response.status_code == 200 and \
        response.json['message'] == "Friendship request sent"


def test_friendship_request_already_sent(client, user, user2, access_token, user_repository):
    client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': user2['id']
    })

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': user2['id']
    })

    db_user = user_repository.get(user['id'])
    db_user2 = user_repository.get(user2['id'])

    assert db_user['sent_friendship_request'] == db_user2['id'] and \
        db_user2['friendship_request'] == db_user['id'] and \
        response.status_code == 400 and \
        response.json['message'] == 'You had already sent a friendship_request for this user'


def test_already_friends(client, user, user2, access_token, user_repository):
    user_repository.update(user['id'], {"friends": user2['id']})
    user_repository.update(user2['id'], {"friends": user['id']})

    db.session.commit()

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': user2['id']
    })


    assert response.status_code == 400 and \
        response.json['message'] == 'You are already friends'
