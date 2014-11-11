from flask.ext import restful
from flask import request

from stormy.app.helpers import api_helpers


class List(restful.Resource):
    def get(self, item_id=None):
        return api_helpers.list_objects(request.path)

