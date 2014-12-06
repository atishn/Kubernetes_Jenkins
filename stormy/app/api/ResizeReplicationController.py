from flask.ext.restful import reqparse, Resource

from app.helpers.api_helpers import resize_replication_controller


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

        resize_replication_controller(args['id'], args['num'])

