## Info
Story Celery app is Python based Utility which facilitates the control of auto scalable Jenkins Master Slave enviornment on the cloud with the Kubernetes orchestration using simplified Kubernetes REST API calls.
Stormy connects to Master node of your Kubernetes cluster, and controls the spinup/ spindown of Jenkins Master and Slave instances as being said it uses Kubernetes supported REST API to do that.

## Stack
    Docker
    Python
    Celery
    REST
    Redis
    Fig



For More info about the Kubernetes, check out https://github.com/GoogleCloudPlatform/kubernetes

Sample list of commands to host and connect to Kubernetes. In this example we are using GCE instances.

	gcloud components update preview
	gcloud preview container clusters list --zone us-central1-f
	gcloud preview container clusters create stormy-opensource --zone us-central1-f --num-nodes 3 --password HmDUZ0u6OVVC
	gcloud preview container clusters list --zone us-central1-f 

Once setup make sure you can connect to Kubernetes Master node using Kubernetes provided REST API. I have shared couple of useful commands with an example of Master KubeIP = 130.211.113.211.

	https://130.211.113.211
	   
	"User": "admin"
	"Password": "HmDUZ0u6OVVC"

You may need to open up ports from Node GCE instances as Jenkins Master and Slave needs to communicated through JNLP.

	gcutil addfirewall --allowed=tcp:49151 --target_tags=k8s-stormy-opensource-node k8s-stormy-opensource-node-49151
	gcutil addfirewall --allowed=tcp:48673 --target_tags=k8s-stormy-opensource-node k8s-stormy-opensource-node-48673
	gcloud preview container pods list --cluster stormy-opensource --zone us-central1-f


Stormy app needs following parameters to start execution.

	1. Kuebernetes Master IP address Eg. 130.211.113.211
	2. Kubernetes User Id       Eg. admin
	3. Kubernetes Password      Eg. HmDUZ0u6OVVC
	4. Jenkins Master Docker Name Eg. master_master
	5. Jenkins Slave Docker Name Eg. slave_slave
	6. Docker registry name( Where Jenkins Master/Slave docker instances pushed) Eg. huge


This app is built with the Docker cluster in mind. But nontheless This app can be run on local by 3 ways.

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

## List of couple of useful commands.

### For Cluster Creation and Deletion

	gcloud preview container clusters create stormy-jerkins --zone us-central1-f —num-nodes 3 —password HmDUZ0u6OVVC
	gcloud preview container clusters delete stormy-jerkins --zone us-central1-f

### For Pods Listing, Deletion.

	gcloud preview container pods list --cluster stormy-jenkins --zone us-central1-f
	gcloud preview container pods describe NAME --cluster stormy-jenkins --zone us-central1-f 
	gcloud preview container pods delete NAME --cluster stormy-jenkins --zone us-central1-f 

### For Replication Controller List, Resize and Deletion.

	gcloud preview container replicationcontrollers list --cluster stormy-jenkins --zone us-central1-f 
	gcloud preview container replicationcontrollers resize NAME --num-replicas 0 --cluster stormy-jenkins --zone us-central1-f 
	gcloud preview container replicationcontrollers delete NAME --cluster stormy-jenkins --zone us-central1-f

### For SSH into the cluster

	gcloud compute  ssh --zone us-central1-f k8s-stormy-jenkins-master
	gcloud compute  ssh --zone us-central1-f k8s-stormy-jenkins-node-1
	gcloud compute  ssh --zone us-central1-f k8s-stormy-jenkins-node-2
 
### If new cluster is created, then couple of ports needs to be open for proper working of Jenkin Pods and Replication Controllers on slave nodes.
	
	gcutil addfirewall --allowed=tcp:49151 --target_tags=k8s-stormy-jenkins-node k8s-stormy-jenkins-node-49151
	gcutil addfirewall --allowed=tcp:48673 --target_tags=k8s-stormy-jenkins-node k8s-stormy-jenkins-node-48673

