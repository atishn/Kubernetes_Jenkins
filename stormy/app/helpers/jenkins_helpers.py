from jenkinsapi.jenkins import Jenkins
from flask import current_app as app

from api_helpers import get_pod_byid, findHostPort


def get_running_jenkins_jobs():
    num_running = 0
    server = get_jenkins_server_instance()
    jobs = server.get_jobs()
    for j in jobs:
        job_instance = server.get_job(j[0])
        if job_instance.is_queued_or_running():
            num_running += 1
    print num_running
    return num_running


def get_jenkins_server_instance():
    pod = get_pod_byid(app.config['JENKINS_MASTER_POD'])
    hostip = findHostPort(pod)
    jenkins_url = 'http://{0}:{1}'.format(hostip, app.config['JENKINS_MASTER_PORT'])  # Eg http://23.251.155.231:49151

    return Jenkins(jenkins_url, username=app.config['JENKINS_USER'], password=app.config['JENKINS_PASS'])