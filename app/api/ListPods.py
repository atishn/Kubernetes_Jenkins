from flask.ext import restful

from flask import current_app as app

import subprocess
import json

import urllib2
import requests

class ListPods(restful.Resource):
    # def get(self):
    #     kube_cfg = app.config['KUBE_ROOT'] + app.config['KUBE_CFG']
    #     cmd = [kube_cfg, '--json', 'list','pods']
    #
    #
    #     proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #     output, err = proc.communicate()
    #
    #     json_output = json.loads(output)
    #     return json_output

    def get(self):
        # urlib2
        # response = urllib2.urlopen(urllib2.Request('https://130.211.122.34/api/v1beta1/pods', headers={'Authorization': 'Basic YWRtaW46OGtXb2lSSFhneE5kMjBkUw=='}))
        # json_resp = json.loads((response.read()))
        # return json_resp

        # requests
        r = requests.get('https://130.211.122.34/api/v1beta1/pods', auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        return r.json()

