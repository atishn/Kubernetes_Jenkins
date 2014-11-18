from flask import Flask
from flask.ext import restful
from oauth2client.tools import argparser
from celery import signals
from celery.bin import Option
from celery.schedules import crontab

from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController
from app.api.List import List
from app.api.Pod import PodHosts
from app.api.ReplicationController import NewSlaveReplication
from app.api.Pod import NewJenkinsMaster
from app.helpers.api_helpers import resize_replication_controller
from app.helpers.celery_helpers import make_celery
from app.helpers.jenkins_helpers import get_running_jenkins_jobs
from app.helpers.api_helpers import get_replication_size


app = Flask(__name__)
api = restful.Api(app)

# Set local vars
# TODO move password out of code
app.config.update(

    KUBE_ROOT='../kubernetes',
    KUBE_CFG='/cluster/kubecfg.sh',
    CELERY_BROKER_URL='redis://146.148.35.179:6379',
    CELERY_RESULT_BACKEND='redis://146.148.35.179:6379',
    CELERYBEAT_SCHEDULE={
        'every-minute': {
            'task': 'stormy_app.check_jobs_and_scale',
            'schedule': crontab(minute='*/1'),
            'args': (),
        },
    },
    JENKINS_USER='',
    JENKINS_PASS='',

    JENKINS_MASTER_POD='jenkinsmaster',
    JENKINS_MASTER_RUNNING_PORT=8090,
    JENKINS_MASTER_PORT=49151,
    JENKINS_MASTER_JNLP_PORT=48673,


    JENKINS_SLAVE_POD_NAME='jenkinsslave',
    JENKINS_SLAVE_CONTROLLER='jenkinsslaveController',
    JENKINS_SLAVE_INIT_SIZE=1,
    DOCKER_REGISTRY='huge'
)

# Stalk
celery = make_celery(app)

celery.user_options['preload'].add(
    Option('-Z', '--master_kube_ip', '--kube_user', '--kube_pass', help='Configuration template to use.'),
    # Option('-Z', '--kube_user', help='Configuration template to use.'),
    # Option('-Z', '--kube_pass', help='Configuration template to use.'),
)


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    app.config['MASTER_IP'] = options['master_kube_ip']
    app.config['API_USER'] = options['kube_user']
    app.config['API_PASS'] = options['kube_pass']
    app.config['JENKINS_MASTER_DOCKER'] = options['master_docker']
    app.config['JENKINS_SLAVE_DOCKER'] = options['slave_docker']


@celery.task()
def check_jobs_and_scale():
    num_running_jobs = get_running_jenkins_jobs()
    if num_running_jobs == 0:
        resize_replication_controller(app.config['JENKINS_SLAVE_POD_NAME'], app.config['JENKINS_SLAVE_CONTROLLER'], 0)
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

api.add_resource(NewJenkinsMaster, '/new/master')
api.add_resource(NewSlaveReplication, '/new/slaves')
# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')


# run pods
api.add_resource(Run, '/run')

app.debug = True

if __name__ == "__main__":
    argparser.add_argument("--master_kube_ip", help="Search term")
    argparser.add_argument("--kube_user", help="Search term")
    argparser.add_argument("--kube_pass", help="Search term")
    argparser.add_argument("--master_docker", help="Search term")
    argparser.add_argument("--slave_docker", help="Search term")

args = argparser.parse_args()
app.config['MASTER_IP'] = args.master_kube_ip
app.config['API_USER'] = args.kube_user
app.config['API_PASS'] = args.kube_pass
app.config['JENKINS_MASTER_DOCKER'] = args.master_docker
app.config['JENKINS_SLAVE_DOCKER'] = args.slave_docker

app.run(host='0.0.0.0')