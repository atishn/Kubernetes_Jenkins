from flask.ext import restful

from flask import current_app as app
from flask import request

import requests

class PodHosts(restful.Resource):

    def get(self, item_id=None):

        print ">>>>atish"
        print item_id

        url = 'https://{0}/api/v1beta1/pods/{1}'.format(app.config['MASTER_IP'], item_id)
        print url

        r = requests.get(url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)

        response = r.json()

        hostIp = response.get('currentState').get('hostIP')

        return hostIp

