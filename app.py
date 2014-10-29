from flask import Flask
from flask.ext import restful

from app.api.ListPods import ListPods
from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController

app = Flask(__name__)
api = restful.Api(app)

# Set local vars
# TODO move password out of code
app.config.update(
    KUBE_ROOT='../kubernetes',
    KUBE_CFG='/cluster/kubecfg.sh',
    API_USER='admin',
    API_PASS='8kWoiRHXgxNd20dS'
)

# list pods - to make sure works
api.add_resource(ListPods, '/list-pods')

# run pods
# /<string:dockerfile>/<string:num_pods>/<string:name>
api.add_resource(Run, '/run')

# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')

app.debug = True

if __name__ == "__main__":
    app.run()