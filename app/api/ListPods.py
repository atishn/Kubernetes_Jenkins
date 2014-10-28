from flask.ext.restful import Resource
import subprocess

class ListPods(Resource):
    def get(self):
        kube_cfg = app.config['KUBE_ROOT'] + '/cluster/kubecfg.sh'
        cmd = [kube_cfg, '--json list pods']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        return output
        
        