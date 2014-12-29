## Use Case
Set up Jenkins Master/Slave environment using Dockerized Kubernetes cluster with Google Cloud Engine (GCE)


This workspace includes, two submodules.

## Jenkins :
This submodule includes the docker workspace of Jenkins Master and Jenkins Slave instances. Jenkins Master open up JNLP port which Slave uses to connect.

Whenever new Slave instances gets spinup , it connect to Master JNLP port and Master configures itself to assign any new additional task.


## Stormy:
Stormy is Python based Celery task runner, which pings Kubernetes cluster and look for any valid instances of Jenkins Master Node. If doesnt found it instructs to download and run the Jenkins Master Pod. Once setup it ping Jenkins Master Node with a continuous interval and look for current queue size. If it finds queue is getting increased, it commands Kubernetes to resize the Jenkins Slave replication controller.
	
So in short stormy jobs can spin up/ spin down slave docker instances as per the queue size.
