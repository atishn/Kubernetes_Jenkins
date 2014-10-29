from flask.ext import restful

from flask import current_app as app
from flask import request

import requests

class List(restful.Resource):

    def get(self, **kwargs):
        url = 'https://{0}/api/v1beta1/{1}'.format(app.config['MASTER_IP'], request.path)

        if 'item_id' in locals():
            url += '/{}'.format(item_id)

        print url

        r = requests.get(url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        return r.json()

