#!/bin/sh
docker build -t jenkins_slave .
docker tag jenkins_slave huge/jenkins_slave_docker
docker push huge/jenkins_slave_docker

