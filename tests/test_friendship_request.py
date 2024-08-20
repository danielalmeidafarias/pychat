import uuid
from app.db import db


def test_send_friendship_request(client, access_token, user, user2, friendship_request_repository):
    sender_id = user['id']
    receiver_id = user2['id']

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'receiver_id': receiver_id
    })

    friendship_request = friendship_request_repository.get_one(receiver_id=receiver_id, sender_id=sender_id)

    assert friendship_request.sender_id == sender_id and \
        friendship_request.receiver_id == receiver_id and \
        response.status_code == 200


def test_friendship_request_already_sent(client, user, user2, access_token, friendship_request_repository):
    sender_id = user['id']
    receiver_id = user2['id']

    client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'receiver_id': receiver_id
    })

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'receiver_id': receiver_id
    })

    friendship_request = friendship_request_repository.get_one(sender_id=sender_id, receiver_id=receiver_id)

    assert friendship_request.sender_id == sender_id and \
        friendship_request.receiver_id == receiver_id and \
        response.status_code == 400 and \
        response.json['message'] == 'You had already sent a friendship request for this user'


def test_already_friends(client, user, user2, access_token, friendship_repository):
    friendship_repository.create(user_id=user['id'], friend_id=user2['id'])

    db.session.commit()

    response = client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'receiver_id': user2['id']
    })

    assert response.status_code == 400 and \
        response.json['message'] == 'You are already friends'


def test_user_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(sender_id=user['id'], receiver_id=user2['id'])

    response = client.get(f"/friendship_request", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['receiver_id'] == user2['id'] and \
        response.json[0]['sender_id'] == user['id']


def test_user_sent_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(sender_id=user['id'], receiver_id=user2['id'])

    response = client.get(f"/friendship_request?sent=True", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['receiver_id'] == user2['id'] and \
        response.json[0]['sender_id'] == user['id']


def test_user_received_friendship_requests(client, user, user2, access_token, friendship_request_repository):
    friendship_request_repository.create(sender_id=user2['id'], receiver_id=user['id'])

    response = client.get(f"/friendship_request?received=True", headers={
        'Authorization': access_token
    })

    assert response.status_code == 200 and \
        len(response.json) == 1 and \
        response.json[0]['receiver_id'] == user['id'] and \
        response.json[0]['sender_id'] == user2['id']


def test_refused_friendship_request(client, user, user2, access_token, friendship_request_repository):
    friendship_request_id = friendship_request_repository.create(sender_id=user2['id'], receiver_id=user['id']).id

    response = client.put(f"/friendship_request/{friendship_request_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'refused'
    })

    assert response.status_code == 200


def test_accepted_friendship_request(client, user, user2, access_token, friendship_request_repository):
    friendship_request_id = friendship_request_repository.create(sender_id=user2['id'],
                                                                 receiver_id=user['id']).id
    response = client.put(f"/friendship_request/{friendship_request_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'accepted'
    })

    assert response.status_code == 200

def test_accepted_and_refused_request(client, user, user2, user3, user4,  access_token, friendship_request_repository):
    friendship_request1_id = friendship_request_repository.create(sender_id=user2['id'], receiver_id=user['id']).id
    friendship_request2_id = friendship_request_repository.create(sender_id=user3['id'], receiver_id=user['id']).id
    friendship_request3_id = friendship_request_repository.create(sender_id=user4['id'], receiver_id=user['id']).id

    client.put(f"/friendship_request/{friendship_request1_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'accepted'
    })
    client.put(f"/friendship_request/{friendship_request2_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'accepted'
    })
    client.put(f"/friendship_request/{friendship_request3_id}", headers={
        "Authorization": access_token
    }, json={
        "status": 'refused'
    })

    response = client.get(f"/friendship_request?status=accepted", headers={
        'Authorization': access_token
    })

    assert response.json[0]['receiver_id'] == user['id'] and \
           response.json[0]['sender_id'] == user2['id'] and \
           response.json[0]['status'] == 'accepted' and \
           response.json[1]['receiver_id'] == user['id'] and \
           response.json[1]['sender_id'] == user3['id'] and \
           response.json[1]['status'] == 'accepted'
