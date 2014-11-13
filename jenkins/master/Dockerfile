FROM ubuntu:14.04
MAINTAINER SysOps "sysops@hugeinc.com"

RUN apt-get update && apt-get install wget -yy
RUN wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
RUN echo "deb http://pkg.jenkins-ci.org/debian binary/" >> /etc/apt/sources.list
RUN apt-get update && apt-get install git jenkins -y

## Create Jenkins Plugin Folder and seed it with Pipeline plugin and dependencies
RUN mkdir -p /var/lib/jenkins/.jenkins/plugins
ADD ./plugins/ /var/lib/jenkins/.jenkins/plugins/


## Time zone
RUN echo America/New York > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata


## Create Jenkins Jobs folder and seeds it with precreated demo jobs
RUN mkdir -p /var/lib/jenkins/.jenkins/jobs
ADD ./jobs/ /var/lib/jenkins/.jenkins/jobs/

## Create Jenkins pipe example config
ADD ./config.xml /var/lib/jenkins/.jenkins/

## Clean up any permission issues
RUN chown -R jenkins:jenkins /var/lib/jenkins

# Exposing Jenkins Port
EXPOSE 8090

# Jenkins is configured with JNLP Slave port in config.xml. Exposing here from slaves access.
EXPOSE 48673

# Run at the entry point
ENTRYPOINT exec su jenkins -c "java -jar /usr/share/jenkins/jenkins.war --httpPort=8090 --ajp13Port=-1"
