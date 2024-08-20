from uuid import UUID

def test_created_chat(app, chat_repository):
    chat = chat_repository.create()

    assert chat is not None
    assert isinstance(UUID(chat['chat_id']), UUID)


def test_chat_members(user, user2, chat_repository, chat_members_repository, user_repository):
    chat_id = chat_repository.create()['chat_id']

    chat_members_repository.create(chat_id=chat_id, user_id=user['id'])
    chat_members_repository.create(chat_id=chat_id, user_id=user2['id'])

    db_user = user_repository.get_one(user['id'])
    db_user2 = user_repository.get_one(user2['id'])

    assert db_user['chats'][0].id == chat_id and \
        db_user['chats'][0].id == chat_id
