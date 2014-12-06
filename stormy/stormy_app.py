from flask import Flask
from flask.ext import restful
from oauth2client.tools import argparser
from celery import signals
from celery.bin import Option
from celery.schedules import crontab
import httplib

from app.api.Run import Run
from app.api.ResizeReplicationController import ResizeReplicationController
from app.api.List import List
from app.api.Pod import PodHosts
from app.api.ReplicationController import NewSlaveReplication
from app.api.Pod import NewJenkinsMaster
from app.helpers.api_helpers import resize_replication_controller
from app.helpers.celery_helpers import make_celery
from app.helpers.jenkins_helpers import get_running_jenkins_jobs
from app.helpers.api_helpers import get_replication_size, get_pod_byid, findHostPort, new_pod

app = Flask(__name__)
api = restful.Api(app)

# Set local vars
# TODO move password out of code
app.config.update(
    DEFAULT_MASTER_KUBE_IP='130.211.122.34',
    KUBE_ROOT='../kubernetes',
    KUBE_CFG='/cluster/kubecfg.sh',
    CELERY_BROKER_URL='redis://redis:6379',
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
)


# Stalk
celery = make_celery(app)

celery.user_options['preload'].add(
    Option('-Z', '--master_kube_ip'),
)

celery.user_options['preload'].add(
    Option('--kube_user'),
)

celery.user_options['preload'].add(
    Option('--kube_pass')
)

celery.user_options['preload'].add(
    Option('--master_docker')
)

celery.user_options['preload'].add(
    Option('--slave_docker')
)

celery.user_options['preload'].add(
    Option('--docker_registry')
)

@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    app.config['MASTER_IP'] = options['master_kube_ip']
    app.config['API_USER'] = options['kube_user']
    app.config['API_PASS'] = options['kube_pass']
    app.config['JENKINS_MASTER_DOCKER'] = options['master_docker']
    app.config['JENKINS_SLAVE_DOCKER'] = options['slave_docker']
    app.config['DOCKER_REGISTRY'] = options['docker_registry']

# def resize_replication_controller(name, controller_id, num, image, ports=[], variables=None):CELERY_BROKER_URL

@celery.task()
def check_jobs_and_scale():
    master_jenkins_pod = get_pod_byid(app.config['JENKINS_MASTER_POD'])

    if master_jenkins_pod.get('code') == httplib.NOT_FOUND:
        new_pod(app.config['JENKINS_MASTER_POD'], app.config['JENKINS_MASTER_DOCKER'], [[app.config['JENKINS_MASTER_RUNNING_PORT'], app.config['JENKINS_MASTER_PORT']], [app.config['JENKINS_MASTER_JNLP_PORT'], app.config['JENKINS_MASTER_JNLP_PORT']]])
    elif master_jenkins_pod.get('currentState').get('status') != 'Running':
        print "Wait for more time until master starts up"
    else:
        podIp = findHostPort(master_jenkins_pod)

        num_running_jobs = get_running_jenkins_jobs()

        if num_running_jobs == 0:
            resize_replication_controller(app.config['JENKINS_SLAVE_POD_NAME'], app.config['JENKINS_SLAVE_CONTROLLER'], 1, app.config['JENKINS_SLAVE_DOCKER'], [], [["JENKINS_MASTER_HOST", podIp], ["JENKINS_MASTER_PORT", app.config['JENKINS_MASTER_PORT']]])
        else:
            current_rc_size = get_replication_size(app.config['JENKINS_SLAVE_CONTROLLER'])
            if current_rc_size < num_running_jobs:
                resize_replication_controller(app.config['JENKINS_SLAVE_POD_NAME'], app.config['JENKINS_SLAVE_CONTROLLER'], num_running_jobs, app.config['JENKINS_SLAVE_DOCKER'], [], [["JENKINS_MASTER_HOST", podIp], ["JENKINS_MASTER_PORT", app.config['JENKINS_MASTER_PORT']]])

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

api.add_resource(NewJenkinsMaster, '/new/master')
api.add_resource(NewSlaveReplication, '/new/slaves')

# resize existing application controller, requires 'id' and 'num' params
api.add_resource(ResizeReplicationController, '/resize')


# run pods
api.add_resource(Run, '/run')

app.debug = True

if __name__ == "__main__":
    argparser.add_argument("--master_kube_ip")
    argparser.add_argument("--kube_user", help="Search term")
    argparser.add_argument("--kube_pass", help="Search term")
    argparser.add_argument("--master_docker", help="Search term")
    argparser.add_argument("--slave_docker", help="Search term")
    argparser.add_argument("--docker_registry", help="Search term")

    args = argparser.parse_args()
    app.config['MASTER_IP'] = args.master_kube_ip
    app.config['API_USER'] = args.kube_user
    app.config['API_PASS'] = args.kube_pass
    app.config['JENKINS_MASTER_DOCKER'] = args.master_docker
    app.config['JENKINS_SLAVE_DOCKER'] = args.slave_docker
    app.config['DOCKER_REGISTRY'] = args.docker_registry

    app.run(host='0.0.0.0')