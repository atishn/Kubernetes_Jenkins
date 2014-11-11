## Info
Story Flask app is Python based Utility which faciliates the handling of Jenkins Kubernetes cluster with simiplified API calls.


The kubernetes master server ('kubernetes-master') has a built in API as described [here](http://cdn.rawgit.com/GoogleCloudPlatform/kubernetes/31a0daae3627c91bc96e1f02a6344cd76e294791/api/kubernetes.html): . It can be accessed via the public ip for the master server. For example [https://130.211.122.34/api/v1beta1/replicationControllers](https://130.211.122.34/api/v1beta1/replicationControllers) will list the current ReplicationControllers. Port 8080 must be opened for that server in GCE. The username and password needed to access the server can be found in the ~/.kubernetes_auth file on your machine (assuming that you followed the directions in '[Setup Kubernetes cluster on local machine](/display/GLCS/Setup+Kubernetes+cluster+on+local+machine)').

We have created this [simple flask app](https://stash.hugeinc.com/projects/GLCS/repos/stormy-flask/browse) that utilizes that api as a POC. The longterm plan is to have these api calls be fired automatically to resize the jenkins slaves based on usage using Celery.

Stormy Flask app and Celery Cron job both needs ip address of master_kube_ip for http connection.

## Run the app:

Download the [repo](https://stash.hugeinc.com/projects/GLCS/repos/stormy-flask/browse) and run:

    brew install redis
    pip install -r requirements.txt
    python stormy_app.py --master_kube_ip 130.211.113.209
    celery -A stormy_app.celery worker --loglevel=info --beat --master_kube_ip=130.211.113.209

# Use Fig App to make your life easy
    fig up

# Add new master
http://localhost:5000/new/master

# Add new slave clusters
http://localhost:5000/new/slaves


##Run the Docker
docker build -t docker_stormy .
docker run -d -p 22 -e "MASTERKUBEIP=130.211.113.209" --name stormy_app -t docker_stormy
docker tag docker_stormy huge/docker_stormy
docker push huge/docker_stormy


### New Pod
Visit http://localhost:5000/new/pod?name=<name>&image=<docker_image_name>&containerPort=<containerPort>&hostPort=<hostPort>. For example:  http://localhost:5000/new/replicationController?name=jenkinsmaster&image=jenkins_pipeline&hostPort=49162&containerPort=8080﻿. Name must be lowercase and will be used for the id, labels and container names.

### List Pods

Visit http://localhost:5000/pods to see a json list of the current pods
Visit http://localhost:5000/pods/<pod_id> to see info for a specific pod

### List Replication Controllers

Visit http://localhost:5000/replicationControllers to see a json list of the current replication controllers
Visit http://localhost:5000/replicationControllers/<replication_controller_id> to see info for a specific replication controller

### New Replication Controller

Visit http://localhost:5000/new/replicationController?name=<name>&image=<docker_image_name>&num=<num_pods>&containerPort=<containerPort>&hostPort=<hostPort>. For example:  http://localhost:5000/new/replicationController?name=jenkinsmaster&image=jenkins_pipeline&num=2&hostPort=49162&containerPort=8080. Name must be lowercase and will be used for the id, labels and container names.

### Resize Replication Controller

Visit http://localhost:5000/resize?id=<controller_name>&num=<new_size>. For example http://localhost:5000/resize?id=jenkinsMasterController&num=0. Will return a json of the current state and the requested state. (Will only work if you have already created a ReplicationController with that id).


### List Services

Visit http://localhost:5000/services to see a json list of the current pods
Visit http://localhost:5000/sevices/<service_id> to see info for a specific pod


## Shortcuts
Visit http://localhost:5000/new/master to start a jenkins master pod with default configuration.
Visit http://localhost:5000/new/slave to start a jenkins slave replicationController with default configuration





