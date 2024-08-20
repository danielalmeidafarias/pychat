def test_created_friendship(friendship_repository, user, user2):
    user_id = user['id']
    friend_id = user2['id']

    friendship_repository.create(user_id=user_id, friend_id=friend_id)

    friendship = friendship_repository.get(user_id=user_id, friend_id=friend_id)
    friendship2 = friendship_repository.get(user_id=friend_id, friend_id=user_id)


    assert friendship[0] == friendship2[1] == user_id and \
        friendship[1] == friendship2[0] == friend_id
