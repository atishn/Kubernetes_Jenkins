from flask.ext.restful import reqparse, Resource

from app.helpers.api_helpers import new_replication_controller, get_pod_byid, findHostPort
from flask import current_app as app


class NewReplicationController(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('num', type=int)
        parser.add_argument('image', type=str)
        parser.add_argument('containerPort', type=int)
        parser.add_argument('hostPort', type=int)
        args = parser.parse_args()

        server_response = new_replication_controller(args['name'], args['num'], args['image'],
                                                     [[args['containerPort'], args['hostPort']]])

        return server_response


class NewSlaveReplication(Resource):
    def get(self):
        pod = get_pod_byid(app.config['JENKINS_MASTER_POD'])
        podIp = findHostPort(pod)

        server_response = new_replication_controller(app.config['JENKINS_SLAVE_POD_NAME'], app.config['JENKINS_SLAVE_CONTROLLER'], app.config['JENKINS_SLAVE_INIT_SIZE'] , app.config['JENKINS_SLAVE_DOCKER'], [], [["JENKINS_MASTER_HOST", podIp],["JENKINS_MASTER_PORT", app.config['JENKINS_MASTER_PORT']]])

        return server_response