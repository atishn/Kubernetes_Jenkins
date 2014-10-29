from flask.ext.restful import reqparse, Resource

import requests
import json

from flask import current_app as app

# request.args.get('myParam')

# cluster/kubecfg.sh -p 8080:80 run ec2-54-82-197-2.compute-1.amazonaws.com:5000/jenkins_pipeline 2 jenkins-master
class ResizeReplicationController(Resource):
    def get(self):
        # TODO and check if id and/or num not passed

        # TODO is there a better way of handling args?
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('num', type=int, help='num_pods cannot be converted')
        args = parser.parse_args()

        controller_url = 'https://{0}/api/v1beta1/replicationControllers/{1}'.format(app.config['MASTER_IP'], args['id'])

        # request = urllib2.Request('https://130.211.122.34/api/v1beta1/replicationControllers/' + args['id'], headers={'Authorization': 'Basic YWRtaW46OGtXb2lSSFhneE5kMjBkUw=='})
        # response = urllib2.urlopen(request)
        # current_contoller = json.loads((response.read()))

        request_controller = requests.get(controller_url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        current_controller =  request_controller.json()

        if current_controller['kind'] == "Status":
            return current_controller

        current_controller['desiredState']['replicas'] = args['num']

        # need to dump to get rid of unicode u'
        new_controller = json.dumps(current_controller)

        put_response = requests.put(controller_url, data=new_controller, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        return put_response.json()


