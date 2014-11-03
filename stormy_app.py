from flask import Flask
from flask.ext import restful

from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController
from app.api.List import List
from app.api.NewReplicationController import NewReplicationController, NewSlaveReplication
from app.api.NewPod import NewPod, NewJenkinsMaster
from app.helpers.api_helpers import resize_replication_controller

from app.helpers.celery_helpers import make_celery
from app.helpers.jenkins_helpers import get_running_jenkins_jobs
from app.helpers.api_helpers import get_replication_size
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
    # API_USER='vagrant',
    # API_PASS='vagrant',
    # MASTER_IP='10.245.1.2',
    DOCKER_REGISTRY='huge',
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
    JENKINS_PASS='',
    JENKINS_SLAVE_CONTROLLER='jenkinsslaveController'
)

# Stalk
celery = make_celery(app)

@celery.task()
def check_jobs_and_scale():
    num_running_jobs = get_running_jenkins_jobs()
    if num_running_jobs == 0:
        resize_replication_controller(app.config['JENKINS_SLAVE_CONTROLLER'], 1)
    else:
        current_rc_size = get_replication_size(app.config['JENKINS_SLAVE_CONTROLLER'])
        if current_rc_size < (num_running_jobs / 5):
            resize_replication_controller(app.config['JENKINS_SLAVE_CONTROLLER'], (num_running_jobs / 5))


# lists:
api.add_resource(List,
                 '/pods',
                 '/replicationControllers',
                 '/services',
                 '/pods/<string:item_id>',
                 '/replicationControllers/<string:item_id>',
                 '/services/<string:item_id>')

# TODO change these to post/put requests
# new - replication controller for now
# requires 'id' and 'num' params
api.add_resource(NewReplicationController, '/new/replicationController')
api.add_resource(NewSlaveReplication, '/new/slaves')

api.add_resource(NewPod, '/new/pod')
api.add_resource(NewJenkinsMaster, '/new/master')

# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')


# run pods
api.add_resource(Run, '/run')

app.debug = True

if __name__ == "__main__":
    app.run()