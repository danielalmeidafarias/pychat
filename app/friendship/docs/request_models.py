from flask_restx import fields, Namespace


class FriendshipRequestModels:
    def __init__(self, nm: Namespace):
        self.create_friendship = nm.model('Create friendship', {})
        self.get_friendship = nm.model('Get friendship', {})
        self.update_friendship = nm.model('Update friendship', {})
        self.delete_friendship = nm.model('Delete friendship', {})
