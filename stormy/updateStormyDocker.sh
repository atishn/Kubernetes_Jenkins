#!/bin/sh
# Example configuration with 'huge' as a Docker Repo.

docker build -t stormy_stormy .
docker tag stormy_stormy huge/stormy_stormy
docker push huge/stormy_stormy