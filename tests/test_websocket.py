def test_message_handler(socketio_client, socketio, app):
    socketio_client.emit('message')
    socketio.handlers()

    client1 = socketio.test_client(app)
    client1.emit('testing')

    received = client1.get_received()

    assert received == ["success"]
