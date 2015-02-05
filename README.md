## Use Case
Set up Auto scalable Jenkins Master/Slave environment using Dockerized Kubernetes cluster on Google Cloud Engine (GCE)


This workspace includes, two submodules.
## 1. Jenkins :
This sub module includes the docker workspace of Jenkins Master and Jenkins Slave instances. Jenkins Master open up JNLP port which Slave tries to connect. Whenever new Slave instances gets spinup , it connect to Master JNLP port and Master configures itself to assign any new additional task.


## 2. Stormy:
Stormy is Python based Celery task runner, which pings Kubernetes cluster and look for any valid instances of Jenkins Master Node. If doesnt, it uses Kubernetes REST API to download and spin up the Jenkins Master Pod and Slave Replication Controller. 
Once setup it ping Jenkins Master Node with a continuous interval and look for current queue size. If it finds queue is getting increased, it instructs Kubernetes to resize the Jenkins Slave replication controller as per need.
