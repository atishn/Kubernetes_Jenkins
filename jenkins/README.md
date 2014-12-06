This workspace is intended to create a Docker Environment with Jenkins setup. This can be very easily configured and modified as per convenience.

This workspace can create docker instances of Jenkins master and Jenkins Slave.


## Stack
Docker
Fig

## To start the docker on local
* boot2docker start   # If using Mach
* sudo docker service start # If using Linux

Docker instances of Master and Slave can be created two ways.

1. Fig.
2. Docker commands.

Using the tool, Fig, everything gets very easy.
# You can also install Fig to avoid such crazy commands
* sudo pip install -U fig


# For quick build and up Master and Slave on local using Fig
* fig up

Note : Fig uses configuration file 'fig.yml' in the docker folder.


#To create and spin up Master docker instances using docker commands
* docker build -t master_masterdocker .
* docker run -d -P -p 48673:48673 -p 49151:8090 --name jenkins_master_instance -t master_masterdocker
* docker ps

Port 48673 has been used for JNLP Client connections and 49151 used for exposure to UI.
Both port must be opened incase you decide to move this docker instance on servers.

#To Start and Stop instances
* docker start jenkins_master_instance
* docker stop jenkins_master_instance


#To create and spin up Slave docker instances using docker commands. With Example
* docker build -t slave_slavedocker .
* docker run -d -P -e "JENKINS_MASTER_HOST=192.168.59.103" -e "JENKINS_MASTER_PORT=49151" --name jenkins_slave_instance -t slave_slavedocker