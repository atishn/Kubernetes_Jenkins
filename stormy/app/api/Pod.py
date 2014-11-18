from flask.ext.restful import reqparse, Resource

from flask.ext import restful

from app.helpers.api_helpers import new_pod

from app.helpers import api_helpers
from flask import current_app as app


class NewPod(Resource):
    def get(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('image', type=str)
        parser.add_argument('containerPort', type=int)
        parser.add_argument('hostPort', type=int)
        args = parser.parse_args()

        server_response = new_pod(args['name'], args['image'], [[args['containerPort'], args['hostPort']]])

        return server_response


class NewJenkinsMaster(Resource):
    def get(self):
        server_response = new_pod(app.config['JENKINS_MASTER_POD'], app.config['JENKINS_MASTER_DOCKER'], [[app.config['JENKINS_MASTER_RUNNING_PORT'], app.config['JENKINS_MASTER_PORT']], [app.config['JENKINS_MASTER_JNLP_PORT'], app.config['JENKINS_MASTER_JNLP_PORT']]])
        return server_response


class PodHosts(restful.Resource):
    def get(self, item_id=None):
        pod = api_helpers.get_pod_byid(item_id)
        hostIp = api_helpers.findHostPort(pod)

        return hostIp

