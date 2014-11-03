import subprocess

from flask.ext.restful import reqparse, Resource
from flask import current_app as app

PORT = '8080:80'

parser = reqparse.RequestParser()



# request.args.get('myParam')

# cluster/kubecfg.sh -p 8080:80 run ec2-54-82-197-2.compute-1.amazonaws.com:5000/jenkins_pipeline 2 jenkins-master
class Run(Resource):
    def get(self):
        # setup parser
        parser = reqparse.RequestParser()
        parser.add_argument('dockerfile', type=str, help='Dockerfile required')
        parser.add_argument('num_pods', type=str, help='num_pods cannot be converted')
        parser.add_argument('name', type=str)
        args = parser.parse_args()


        kube_cfg = app.config['KUBE_ROOT'] + app.config['KUBE_CFG']
        cmd = [kube_cfg, '--json', '-p', PORT,'run', args['dockerfile'], args['num_pods'], args['name']]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, err = proc.communicate()

        print output
        return output