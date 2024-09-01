from flask_restx import Namespace


class MessageRequestModels:
    def __init__(self, nm: Namespace):
        self.create_message = nm.model('Create message', {})
        self.get_message = nm.model('Get message', {})
        self.update_message = nm.model('Update message', {})
        self.delete_message = nm.model('Delete message', {})
