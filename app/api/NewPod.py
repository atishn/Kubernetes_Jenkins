from flask.ext.restful import reqparse, Resource

from flask import current_app as app
from app.helpers.api_helpers import new_pod

class NewPod(Resource):

    def get(self, **kwargs):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('image', type=str)
        parser.add_argument('containerPort', type=str)
        parser.add_argument('hostPort', type=str)
        args = parser.parse_args()

        server_response = new_pod(args['name'], args['image'], args['containerPort'], args['hostPort'])

        return server_response
