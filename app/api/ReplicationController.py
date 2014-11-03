from flask.ext.restful import reqparse, Resource

from app.helpers.api_helpers import new_replication_controller, get_pod_byid, findHostPort


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
        pod = get_pod_byid('jenkinsmaster')
        podIp = findHostPort(pod)

        server_response = new_replication_controller('jenkinsslave', 1, 'jenkins_slave_docker', [[48673, 48673]],
                                                     [["MASTERHOST", podIp]])

        return server_response