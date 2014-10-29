from flask.ext.restful import reqparse, Resource

from flask import current_app as app
from flask import request

import requests
import json

class NewReplicationController(Resource):

    def get(self, **kwargs):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('num', type=int)
        parser.add_argument('image', type=str)
        args = parser.parse_args()

        req_obj = {
            "id": args['name'] + 'Controller',
            "apiVersion": "v1beta1",
            "kind": "ReplicationController",
            "desiredState": {
              "replicas": args['num'],
              "replicaSelector": {"name": args['name']},
              "podTemplate": {
                "desiredState": {
                   "manifest": {
                     "version": "v1beta1",
                     "id": args['name'] + "Controller",
                     "containers": [{
                       "name": args['name'],
                       "image": app.config['DOCKER_REGISTRY'] + '/' + args['image'],
                       "ports": [{"containerPort": 80, "hostPort": 8080}]
                     }]
                   }
                 },
                 "labels": {"name": args['name']}
                }},
            "labels": {"name": args['name']}
          }


        req_json = json.dumps(req_obj)


        url = 'https://{0}/api/v1beta1/replicationControllers'.format(app.config['MASTER_IP'])

        print req_json

        r = requests.post(url, data=req_json, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
        return r.json()