from flask_restx import fields, Namespace


class Friendship_requestRequestModels:
    def __init__(self, nm: Namespace):
        self.create_friendship_request = nm.model('Create friendship_request', {})
        self.get_friendship_request = nm.model('Get friendship_request', {})
        self.update_friendship_request = nm.model('Update friendship_request', {})
        self.delete_friendship_request = nm.model('Delete friendship_request', {})
