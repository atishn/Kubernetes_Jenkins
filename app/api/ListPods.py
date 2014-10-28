from flask.ext.restful import Resource
import subprocess
import json

class ListPods(Resource):
    def get(self):
        kube_cfg = '../kubernetes/cluster/kubecfg.sh'
        cmd = [kube_cfg, '--json', 'list','pods']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, err = p.communicate()
        print output
        json_output = json.loads(output)
        return json_output