This workspace is intended to create a Docker Environment with Jenkins setup. This can be very easily customized as per convenience. This workspace can create docker instances of Jenkins master and Jenkins Slave.
Master uses JNLP Port to connect to slaves. Swarm plugin has been used to facilitate the Master Slave setup.

## Stack
	Docker
	Fig

## To start the docker on local
	 * boot2docker start   # If using Mach
	 * sudo docker service start # If using Linux

Docker instances of Master and Slave can spin up by two ways.

1. Fig.
2. Docker commands.

Its preferred to use the tool, Fig, everything gets very easy.
	sudo pip install -U fig

# For quick build and spin up Master and Slave on local, execute following command in Master and Slave folder.
	fig up

Note : Fig uses configuration file 'fig.yml' in the docker folder.


#To create and spin up Master docker instances using docker commands
	* docker build -t master_master .
	* docker run -d -P -p 48673:48673 -p 49151:8090 --name jenkins_master_instance -t master_master
	* docker ps

Port 48673 has been used for JNLP Client connections and 49151 used for exposure to UI.
Both port must be opened incase you decide to move this docker instance on servers.

#To Start and Stop instances
	* docker start jenkins_master_instance
	* docker stop jenkins_master_instance


#To create and spin up Slave docker instances using docker commands. With Example
* docker build -t slave_slave .
* docker run -d -P -e "JENKINS_MASTER_HOST=192.168.59.103" -e "JENKINS_MASTER_PORT=49151" --name jenkins_slave_instance -t slave_slave


You need to push all these docker instances on some open or private docker registry, so Stormy Kubernetes cluster can download.

## To Push Docker image on Docker Registry
	* docker tag master_master xxxxx/master_master
	* docker push xxxxx/master_master

	* docker tag slave_slave xxxxx/slave_slave
	* docker push xxxxx/slave_slave
