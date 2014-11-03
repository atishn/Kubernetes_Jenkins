from flask import Flask
from flask.ext import restful

from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController
from app.api.List import List
from app.api.Pod import PodHosts
from app.api.ReplicationController import NewReplicationController, NewSlaveReplication
from app.api.Pod import NewPod, NewJenkinsMaster
from app.api.Services import NewService, NewMasterService
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
    MASTER_IP='130.211.122.34',

    KUBE_ROOT='../kubernetes',
    KUBE_CFG='/cluster/kubecfg.sh',
    API_USER='admin',
    API_PASS='8kWoiRHXgxNd20dS',
    # API_USER='vagrant',
    # API_PASS='vagrant',
    # MASTER_IP='10.245.1.2',
    DOCKER_REGISTRY='huge',
    CELERY_BROKER_URL='redis://146.148.35.179:6379',
    CELERY_RESULT_BACKEND='redis://146.148.35.179:6379',
    CELERYBEAT_SCHEDULE = {
        'every-minute': {
            'task': 'stormy_app.check_jobs_and_scale',
            'schedule': crontab(minute='*/1'),
            'args': (),
        },
    },
    #JENKINS_URL='http://23.251.155.231:49151/',
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
        resize_replication_controller(app.config['JENKINS_SLAVE_CONTROLLER'], 0)
    else:
        current_rc_size = get_replication_size(app.config['JENKINS_SLAVE_CONTROLLER'])
        if current_rc_size < num_running_jobs:
            resize_replication_controller(app.config['JENKINS_SLAVE_CONTROLLER'], num_running_jobs)


# lists:
api.add_resource(List,
                 '/pods',
                 '/replicationControllers',
                 '/services',
                 '/pods/<string:item_id>',
                 '/replicationControllers/<string:item_id>',
                 '/services/<string:item_id>')


api.add_resource(PodHosts,
                 '/pods/<string:item_id>/hostIP')

# TODO change these to post/put requests
# new - replication controller for now
# requires 'id' and 'num' params
api.add_resource(NewReplicationController, '/new/replicationController')

api.add_resource(NewPod, '/new/pod')
api.add_resource(NewService, '/new/service')
api.add_resource(NewMasterService, '/new/service-master')


api.add_resource(NewJenkinsMaster, '/new/master')
api.add_resource(NewSlaveReplication, '/new/slaves')



# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')


# run pods
api.add_resource(Run, '/run')

app.debug = True

if __name__ == "__main__":
    app.run()