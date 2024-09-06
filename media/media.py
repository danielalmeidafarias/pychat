from flask_restx import Namespace, Resource, fields
from flask import send_file

media_namespace = Namespace('media')
@media_namespace.route('/300/<user_id>')
class Media300Resource(Resource):
    def get(self, user_id):
        try:
            return send_file(f"../media/300/300_{user_id}.png", mimetype='image/jpeg')
        except FileNotFoundError:
            return {"message": "File not found"}, 404

@media_namespace.route('/150/<user_id>')
class Media150Resource(Resource):
    def get(self, user_id):
        try:
            return send_file(f"../media/150/150_{user_id}.png", mimetype='image/jpeg')
        except FileNotFoundError:
            return {"message": "File not found"}, 404

@media_namespace.route('/50/<user_id>')
class Media50Resource(Resource):
    def get(self, user_id):
        try:
            return send_file(f"../media/50/50_{user_id}.png", mimetype='image/jpeg')
        except FileNotFoundError:
            return {"message": "File not found"}, 404
