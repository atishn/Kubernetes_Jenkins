#!/bin/sh
docker build -t slave_slave .
docker tag slave_slave huge/slave_slave
docker push huge/slave_slave