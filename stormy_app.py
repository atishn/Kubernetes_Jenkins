from flask import Flask
from flask.ext import restful

from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController
from app.api.List import List
from app.api.NewReplicationController import NewReplicationController
from app.helpers.api_helpers import resize_replication_controller

from app.helpers.celery_helpers import make_celery
from app.helpers.jenkins_helpers import get_running_jenkins_jobs
from celery.schedules import crontab

app = Flask(__name__)
api = restful.Api(app)

# Set local vars
# TODO move password out of code
app.config.update(
    KUBE_ROOT='../kubernetes',
    KUBE_CFG='/cluster/kubecfg.sh',
    API_USER='admin',
    API_PASS='8kWoiRHXgxNd20dS',
    MASTER_IP='130.211.122.34',
    DOCKER_REGISTRY='ec2-54-82-197-2.compute-1.amazonaws.com:5000',
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERYBEAT_SCHEDULE = {
        'every-minute': {
            'task': 'stormy_app.check_jobs_and_scale',
            'schedule': crontab(minute='*/1'),
            'args': (),
        },
    },
    JENKINS_URL='http://nyicolo-dev87.ad.hugeinc.com/',
    JENKINS_USER='',
    JENKINS_PASS=''
)

# Stalk
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    res = a + b
    print res
    return res

@celery.task()
def check_jobs_and_scale():
    num_running_jobs = get_running_jenkins_jobs()
    resize_replication_controller('jenkinsmasterController', num_running_jobs + 1)


# lists:
api.add_resource(List,
                 '/pods',
                 '/replicationControllers',
                 '/services',
                 '/pods/<string:item_id>',
                 '/replicationControllers/<string:item_id>',
                 '/services/<string:item_id>')

# new - replication controller for now
# requires 'id' and 'num' params
api.add_resource(NewReplicationController,
                 '/new/replicationController')

# run pods
api.add_resource(Run, '/run')

# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')

app.debug = True

if __name__ == "__main__":
    app.run()