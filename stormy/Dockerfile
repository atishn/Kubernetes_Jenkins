FROM ubuntu:14.04

MAINTAINER HUGE "sysops@hugeinc.com"

#Install Python Dependencies
RUN echo "deb http://pkg.jenkins-ci.org/debian binary/" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install git python python python-dev python-distribute python-pip wget curl -y

# Created User
RUN useradd -ms /bin/bash stormy
ENV HOME /home/stormy


# Created required APP Folders
RUN mkdir -p /home/stormy/stormy-flask/app

# Copy work directory and Install required dependencies
ADD ./app/ /home/stormy/stormy-flask/app
ADD ./stormy_app.py /home/stormy/stormy-flask/
ADD ./requirements.txt /home/stormy/stormy-flask/
RUN pip install -r /home/stormy/stormy-flask/requirements.txt

# Change the User to Stormy
USER stormy

#Create a Celery logs folder
RUN mkdir -p ~/celery

# Change the working director to the app
WORKDIR /home/stormy/stormy-flask

#Run the Celery Batch Job
CMD celery -A stormy_app.celery worker --loglevel=info --beat --master_kube_ip=$MASTERKUBEIP --kube_user=$USERID --kube_pass=$PASSKEY -l info -n name --logfile=~/celery/celery.log --pidfile=~/celery/celery.log --schedule=~/celery/beat.db