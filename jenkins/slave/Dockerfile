FROM ubuntu:14.04
MAINTAINER SysOps "sysops@hugeinc.com"

RUN apt-get update && apt-get install wget curl telnet default-jdk -yy

## Time zone
RUN echo America/New York > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata


#Download Swarm Client
RUN curl -O "http://maven.jenkins-ci.org/content/repositories/releases/org/jenkins-ci/plugins/swarm-client/1.21/swarm-client-1.21-jar-with-dependencies.jar"

#Connect to Swarm to Jenkins Master Client. For now we need to hard code Jenkins Master address.
ENTRYPOINT java -jar swarm-client-1.21-jar-with-dependencies.jar -executors 1 -master http://$JENKINS_MASTER_HOST:$JENKINS_MASTER_PORT -labels ubuntu
