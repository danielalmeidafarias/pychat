import uuid
from app.db import db


def test_send_friendship_request(client, access_token, user, user2, friendship_request_repository):
    sender_id = user['id']
    recipient_id = user2['id']

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': recipient_id
    })

    friendship_request = friendship_request_repository.get_one(recipient_id=recipient_id, sender_id=sender_id)

    assert friendship_request.sender_id == sender_id and \
        friendship_request.recipient_id == recipient_id and \
        response.status_code == 200


def test_friendship_request_already_sent(client, user, user2, access_token, friendship_request_repository):
    sender_id = user['id']
    recipient_id = user2['id']

    client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': recipient_id
    })

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': recipient_id
    })

    friendship_request = friendship_request_repository.get_one(sender_id=sender_id, recipient_id=recipient_id)

    assert friendship_request.sender_id == sender_id and \
        friendship_request.recipient_id == recipient_id and \
        response.status_code == 400 and \
        response.json['message'] == 'You had already sent a friendship request for this user'


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


def test_user_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(id=str(uuid.uuid4()), sender_id=user['id'], recipient_id=user2['id'])

    response = client.get(f"/friendship_request", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['recipient_id'] == user2['id'] and \
        response.json[0]['sender_id'] == user['id']


def test_user_sent_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(id=str(uuid.uuid4()), sender_id=user['id'], recipient_id=user2['id'])

    response = client.get(f"/friendship_request?sent=True", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['recipient_id'] == user2['id'] and \
        response.json[0]['sender_id'] == user['id']


def test_user_received_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(id=str(uuid.uuid4()), sender_id=user2['id'], recipient_id=user['id'])

    response = client.get(f"/friendship_request?received=True", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['recipient_id'] == user['id'] and \
        response.json[0]['sender_id'] == user2['id']


def test_refused_friendship_request(client, user, user2, access_token, friendship_request_repository):
    friendship_request_id = friendship_request_repository.create(id=str(uuid.uuid4()), sender_id=user2['id'], recipient_id=user['id']).id

    response = client.put(f"/friendship_request/{friendship_request_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'refused'
    })

    assert response.status_code == 200


def test_accepted_friendship_request(client, user, user2, access_token, friendship_request_repository):
    friendship_request_id = friendship_request_repository.create(id=str(uuid.uuid4()), sender_id=user2['id'],
                                                                 recipient_id=user['id']).id
    response = client.put(f"/friendship_request/{friendship_request_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'accepted'
    })

    assert response.status_code == 200
