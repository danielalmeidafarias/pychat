from flask_restx import fields, Namespace


class FriendshipResponseModels:
    def __init__(self, nm: Namespace):

        self.post_201 = nm.model(name='friendship_post_201_model', model={
            'message': fields.Raw(''),
        })

        self.post_409 = nm.model(name='friendship_post_409_model', model={
            'message': fields.Raw('')
        })

        self.get_200 = nm.model(name='friendship_get_200', model={
            'message': fields.Raw('')
        })

