from flask.ext import restful
from flask import request

from app.helpers import api_helpers


class List(restful.Resource):
    def get(self):
        return api_helpers.list_objects(request.path)

