from flask_restx import fields, Namespace


class Chat_membersRequestModels:
    def __init__(self, nm: Namespace):
        self.create_chat_members = nm.model('Create chat_members', {})
        self.get_chat_members = nm.model('Get chat_members', {})
        self.update_chat_members = nm.model('Update chat_members', {})
        self.delete_chat_members = nm.model('Delete chat_members', {})
