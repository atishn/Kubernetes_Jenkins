This workspace is intended to create a Docker Environment with Jenkins setup. This can be very easily configured and modified as per convenience.

This workspace can create Jenkins master and also spinup jenkins slaves nodes. It uses Jenkins Swarm plugin to facilitate elastic cluster.

Pre-requisite for local setup:
  1. Mac/Linux
  2. Docker


Commands:

Go to 'master' Folder

* boot2docker start   # If using Mach
* sudo docker service start # If using Linux

#Follow export commands

* docker build -t jenkins_master .
* docker run -d -P -p 0.0.0.0:48673:48673 --name jenkins_master_instance -t jenkins_master
* docker port jenkins_master_instance 8090
* docker ps


To Push Docker image on Docker Registry

* docker tag jenkins_master huge/jenkins_master_docker
* docker push huge/jenkins_master_docker
#If push command fails, make sure you have valid docker id and added to docker registry with permissions.


To Spin up slaves, make sure you updated master docker ip address.
* docker build -t jenkins_slave .
* docker run -d -P -e "MASTERHOST=<Jenkins-MASTERIP>" --name jenkins_slave_instance -t jenkins_slave

To Push Docker image on Docker Registry

* docker tag jenkins_slave huge/jenkins_slave_docker
* docker push huge/jenkins_slave_docker



To Start and Stop instances
* docker start jenkins_master_instance
* docker stop jenkins_master_instance

List all instances
* docker ps -a



