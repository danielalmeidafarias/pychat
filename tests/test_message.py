def test_created_message(message_repository, chat_repository, user):
    chat_id = chat_repository.create()['chat_id']
    message = message_repository.create(chat_id=chat_id, user_id=user['id'], content="Testando mensagem")

    assert message["content"] == "Testando mensagem" and \
        message["chat_id"] == chat_id and \
        message["user_id"] == user['id']

def test_created_message_in_db(message_repository, chat_repository, user):
    chat_id = chat_repository.create()['chat_id']
    message = message_repository.create(chat_id=chat_id, user_id=user['id'], content="Testando mensagem")

    db_message = message_repository.get_one(message_id=message['message_id'])

    assert db_message['content'] == "Testando mensagem"

