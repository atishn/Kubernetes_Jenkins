#!/bin/sh
docker build -t jenkins_master .
docker tag jenkins_master huge/jenkins_master_docker
docker push huge/jenkins_master_docker

