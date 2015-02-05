## Info
Story Celery app is Python based Utility which facilitates the handling of Jenkins Master slave enviornment with Kubernetes cluster.
Stormy connects to Master node of your Kubernetes GCE cluster, and controls the spinup/ spindown of Jenkins Master and Slave pod instances through Kubernetes supported REST API.

## Stack
    Docker
    Python
    Celery
    Flask
    REST
    Redis
    Fig

Note : Stormy Flask app and Celery Cron job both needs ip address of master_kube_ip for http connection.
You need to make sure you have valid Kubernetes cluster setup with up and running Master and Minion Nodes.

For More info about setup, check out https://github.com/GoogleCloudPlatform/kubernetes

List of commands to setup.
gcloud components update preview
gcloud preview container clusters list --zone us-central1-f
gcloud preview container clusters create stormy-opensource --zone us-central1-f --num-nodes 3 --password HmDUZ0u6OVVC

gcloud preview container clusters list --zone us-central1-f
k8s-stormy-opensource-master us-central1-f	k8s-stormy-opensource-master default 130.211.113.211

Once setup make sure you can connect to Kubernetes Master node using Kubernetes provided REST API.

I have shared couple of useful commands with an example of Master KubeIP = 130.211.113.211.

https://130.211.113.211
   
"User": "admin",
"Password": "HmDUZ0u6OVVC",

You may need to open up ports from Node GCE instances as Jenkins Master and Slave needs to communicated through JNLP.

gcutil addfirewall --allowed=tcp:49151 --target_tags=k8s-stormy-opensource-node k8s-stormy-opensource-node-49151
gcutil addfirewall --allowed=tcp:48673 --target_tags=k8s-stormy-opensource-node k8s-stormy-opensource-node-48673

gcloud preview container pods list --cluster stormy-opensource --zone us-central1-f


The kubernetes master server ('kubernetes-master') has a built in API as described [here](http://cdn.rawgit.com/GoogleCloudPlatform/kubernetes/31a0daae3627c91bc96e1f02a6344cd76e294791/api/kubernetes.html): . It can be accessed via the public ip for the master server. 
Stromy uses this REST API to add Master and Slave pods on to the cluster.

There are additional parameters needed to run Stormy.

List of all parameters needed
1. Kuebernetes Master IP address Eg. 130.211.113.211
2. Kubernetes User Id       Eg. admin
3. Kubernetes Password      Eg. HmDUZ0u6OVVC
4. Jenkins Master Docker Name Eg. master_master
5. Jenkins Slave Docker Name Eg. slave_slave
6. Docker registry name( Where Jenkins Master/Slave docker instances pushed) Eg. huge


This app can be run on local by 3 ways.

1. Using Fig. # This one is good for quick local spinup
2. Using Raw Docker commands. # This one is good when you build docker images and update it.
3. Using Celery Python app.  # This one is good for debugging and developing application


## Way 1
##Install Fig
    sudo pip install -U fig

# Use Fig App to make your life easy and run the docker
    fig up
    
## Way 2
##Run the Docker traditional way if fig is not used
    docker build -t stormy_celery .
    docker run -d --name stormy_redis redis:2.8.17
    docker run -e "MASTERKUBEIP=130.211.113.211" -e "USERID=admin" -e "PASSKEY=HmDUZ0u6OVVC" -e "MASTERDOCKER=master_master" -e "SLAVEDOCKER=slave_slave" -e "DOCKERREGISTRY=huge" --name stormy_app --link stormy_redis:redis -t stormy_celery


## Way 3
## Run the app using python:

Download the [repo](https://stash.hugeinc.com/projects/GLCS/repos/stormy-flask/browse) and run:

    brew install redis
    redis-server /usr/local/etc/redis.conf # This may very.
    
    pip install -r requirements.txt
    Add entry of  127.0.0.1 redis in /etc/hosts . If you are running redis on different server , please update it.
    cd app
    celery -A stormy_app.celery worker --loglevel=info --beat --master_kube_ip=130.211.113.211 --kube_user=admin --kube_pass=HmDUZ0u6OVVC --master_docker=master_master --slave_docker=slave_slave --docker_registry=huge


## Build the Image and push to docker registry
    docker tag stormy_celery xxxxx/stormy_celery
    docker push xxxxx/stormy_celery

## To run the app On Stormy Server ( For first time)
    docker run -d --name stormy_redis redis:2.8.17  # Need redis docker instance running
    docker run -d -e "MASTERKUBEIP=130.211.113.211" -e "USERID=admin" -e "PASSKEY=HmDUZ0u6OVVC" -e "MASTERDOCKER=master_master" -e "SLAVEDOCKER=slave_slave" -e "DOCKERREGISTRY=huge" --name stormy_app --link stormy_redis:redis -t huge/stormy_celery

## To update the app on stormy subsequently.
    sh updateStormyDocker.sh

You can also see flask app configuration but its not in use any more, as Celery jobs takes care of everything. This Stormy docker can be run on local or any other cluster node.
Its preferred to spin separate core-os node where stormy can run.


Couple of useful commands.

gcloud preview container replicationcontrollers list --cluster stormy-opensource --zone us-central1-f 
gcloud preview container replicationcontrollers resize jenkinsslaveController  --num-replicas 0 --cluster stormy-opensource --zone us-central1-f 
gcloud preview container replicationcontrollers delete jenkinsslaveController --cluster stormy-opensource --zone us-central1-f

gcloud preview container pods list --cluster stormy-opensource --zone us-central1-f
gcloud preview container pods delete jenkinsmaster --cluster stormy-opensource --zone us-central1-f  


gcloud compute ssh --zone us-central1-f k8s-stormy-opensource-node-2

