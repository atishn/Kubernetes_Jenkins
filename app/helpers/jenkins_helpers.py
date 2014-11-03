from jenkinsapi.jenkins import Jenkins

from flask import current_app as app

def get_running_jenkins_jobs():
    num_running = 0
    server = get_jenkins_server_instance()
    jobs = server.get_jobs()
    for j in jobs:
        job_instance = server.get_job(j[0])
        if job_instance.is_running():
            num_running += 1
    print num_running
    return num_running


def get_jenkins_server_instance():
    jenkins_url = app.config['JENKINS_URL']
    server = Jenkins(jenkins_url, username = app.config['JENKINS_USER'], password = app.config['JENKINS_PASS'])
    return server