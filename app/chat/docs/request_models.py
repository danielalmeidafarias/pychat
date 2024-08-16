from flask_restx import fields, Namespace


class ChatRequestModels:
    def __init__(self, nm: Namespace):
        self.create_chat = nm.model('Create chat', {})
        self.get_chat = nm.model('Get chat', {})
        self.update_chat = nm.model('Update chat', {})
        self.delete_chat = nm.model('Delete chat', {})
