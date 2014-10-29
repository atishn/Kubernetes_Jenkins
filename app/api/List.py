from flask.ext import restful

from flask import current_app as app
from flask import request

import requests

class List(restful.Resource):

    def get(self):
        r = requests.get('https://130.211.122.34/api/v1beta1/' + request.path, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        return r.json()

