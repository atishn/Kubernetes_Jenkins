FROM ubuntu:14.04

MAINTAINER HUGE "sysops@hugeinc.com"

#Install Python Dependencies
RUN echo "deb http://pkg.jenkins-ci.org/debian binary/" >> /etc/apt/sources.list
RUN apt-get update && apt-get install git python python python-dev python-distribute python-pip wget curl telnet -y

# Created User
RUN useradd -ms /bin/bash stormy
ENV HOME /home/stormy


# Created required APP Folders
RUN mkdir -p /home/stormy/stormy-flask/app

# Copy work directory and Install required dependencies
ADD ./app/ /home/stormy/stormy-flask/app
RUN pip install -r /home/stormy/stormy-flask/app/requirements.txt

# Change the User to Stormy
USER stormy

#Create a Celery logs folder
RUN mkdir -p /home/stormy/celery

# Change the working director to the app
WORKDIR /home/stormy/stormy-flask/app

#Run the Celery Batch Job
CMD celery -A stormy_app.celery worker --loglevel=info --beat --master_kube_ip=$MASTERKUBEIP --kube_user=$USERID --kube_pass=$PASSKEY --master_docker=$MASTERDOCKER --slave_docker=$SLAVEDOCKER --docker_registry=$DOCKERREGISTRY -l info -n name --logfile=~/celery/celery.log --pidfile=~/celery/celery.log --schedule=~/celery/beat.db