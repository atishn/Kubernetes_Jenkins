FROM ubuntu:14.04
MAINTAINER SysOps "sysops@hugeinc.com"


## Time zone
RUN echo America/New York > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata


RUN apt-get update && apt-get install wget -yy
RUN wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
RUN echo "deb http://pkg.jenkins-ci.org/debian binary/" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y -qq --no-install-recommends git jenkins curl telnet unzip openssh-client && apt-get clean

# Change to user Jenkins for downloading plugins
USER jenkins

# Download plugins
RUN mkdir -p /var/lib/jenkins/plugins_script
ADD ./plugins_script /var/lib/jenkins/plugins_script/
RUN sh /var/lib/jenkins/plugins_script/download_plugins.sh

## Create Jenkins Plugin Folder and seed it with Pipeline plugin and dependencies
RUN mkdir -p /var/lib/jenkins/.jenkins/plugins

#Copy Downloaded plugins to Jenkins Plugin
RUN cp -r /var/lib/jenkins/downloaded_plugins/* /var/lib/jenkins/.jenkins/plugins/


## Update user back to root.
USER root


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
