from flask.ext.restful import reqparse, Resource

from flask import current_app as app
from app.helpers.api_helpers import new_replication_controller

import requests
import json

class NewReplicationController(Resource):

    def get(self, **kwargs):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('num', type=int)
        parser.add_argument('image', type=str)
        args = parser.parse_args()

        server_response = new_replication_controller(args['name'], args['num'], args['image'])

        return server_response