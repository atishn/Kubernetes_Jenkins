## Info
Story Celery app is Python based Utility which facilitates the handling of Jenkins Master slave enviornment with Kubernetes cluster using simplified API calls.
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
Once setup make sure you can connect to Kubernetes Master node using Kubernetes provided REST API.

I have shared couple of useful commands with an example of Master KubeIP = 130.211.113.211.

https://130.211.113.211/api/v1beta1/pods/jenkinsmaster
It needs userid and password , which can be find in home folder, eg.  cat ~/.kubernetes_auth if you set up Kubernetes cluster from your local.
Eg.   
"User": "admin",
"Password": "8kWoiRHXgxNd20dS",

YOu may need to open up port 8080 from GCE instances.

The kubernetes master server ('kubernetes-master') has a built in API as described [here](http://cdn.rawgit.com/GoogleCloudPlatform/kubernetes/31a0daae3627c91bc96e1f02a6344cd76e294791/api/kubernetes.html): . It can be accessed via the public ip for the master server. 
For example [https://130.211.122.34/api/v1beta1/replicationControllers](https://130.211.122.34/api/v1beta1/replicationControllers) will list the current ReplicationControllers. 
The username and password needed to access the server can be found in the ~/.kubernetes_auth file on your machine (assuming that you followed the directions in '[Setup Kubernetes cluster on local machine](/display/GLCS/Setup+Kubernetes+cluster+on+local+machine)').

There are additional parameters needed to run Stormy.
List of all parameters needed
1. Kuebernetes Master IP address Eg. 130.211.113.211
2. Kubernetes User Id       Eg. admin
3. Kubernetes Password      Eg. 8kWoiRHXgxNd20dS
4. Jenkins Master Docker Name Eg. master_master
5. Jenkins Slave Docker Name Eg. slave_slave
6. Docker registry name( Where Jenkins Master/Slave docker instances pushed) Eg. xxxxx


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
    docker build -t stormy_stormy .
    docker run -d --name stormy_redis redis:2.8.17
    docker run -e "MASTERKUBEIP=130.211.113.211" -e "USERID=admin" -e "PASSKEY=8kWoiRHXgxNd20dS" -e "MASTERDOCKER=master_master" -e "SLAVEDOCKER=slave_slave" -e "DOCKERREGISTRY=huge" --name stormy_app --link stormy_redis:redis -t stormy_stormy

## Way 3
## Run the app using python:

Download the [repo](https://stash.hugeinc.com/projects/GLCS/repos/stormy-flask/browse) and run:

    brew install redis
    pip install -r requirements.txt
    ## Add entry of  146.148.35.179 redis in /etc/hosts . If you are running redis on different server , please update it.
    celery -A stormy_app.celery worker --loglevel=info --beat --master_kube_ip=130.211.113.211 --kube_user=admin --kube_pass=8kWoiRHXgxNd20dS --master_docker=master_master --slave_docker=slave_slave --docker_registry=huge
    #python stormy_app.py --master_kube_ip=130.211.113.211 --kube_user=admin --kube_pass=8kWoiRHXgxNd20dS --master_docker=master_master --slave_docker=slave_slave



## Build the Image and push to docker registry
    docker tag stormy_stormy xxxxx/stormy_stormy
    docker push xxxxx/stormy_stormy


## To run the app On Stormy Server ( For first time)
    docker run -d --name stormy_redis redis:2.8.17  # Need redis docker instance running
    docker run -d -e "MASTERKUBEIP=130.211.113.211" -e "USERID=admin" -e "PASSKEY=8kWoiRHXgxNd20dS" -e "MASTERDOCKER=master_master" -e "SLAVEDOCKER=slave_slave" -e "DOCKERREGISTRY=huge" --name stormy_app --link stormy_redis:redis -t huge/stormy_stormy

## To update the app on stormy subsequently.
    sh updateStormyDocker.sh

You can also see flask app configuration but its not in use any more, as Celery jobs takes care of everything.
But in case for local testing and debug, we need rest endpoints, so it still can be used.
