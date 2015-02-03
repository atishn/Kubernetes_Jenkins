#!/bin/sh
docker build -t master_master .
docker tag master_master huge/master_master
docker push huge/master_master

