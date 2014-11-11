from flask.ext.restful import reqparse, Resource

from flask.ext import restful

from stormy.app.helpers.api_helpers import new_pod

from stormy.app.helpers import api_helpers


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
        server_response = new_pod('jenkinsmaster', 'jenkins_master_docker', [[8090, 49151], [48673, 48673]])
        return server_response


class PodHosts(restful.Resource):
    def get(self, item_id=None):
        pod = api_helpers.get_pod_byid(item_id)
        hostIp = api_helpers.findHostPort(pod)

        return hostIp

