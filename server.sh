#!/bin/sh
# gcloud compute ssh --zone us-central1-b stormy
#docker pull huge/docker_stormy
#docker run -d -p 22 -p 5000:5000 -e "MASTERKUBEIP=130.211.113.209" --name stormy_app -t huge/docker_stormy

gcloud compute ssh --zone us-central1-b stormy --command 'docker pull huge/docker_stormy && docker stop stormy_app && docker rm stormy_app && docker run -d -p 22 -p 5000:5000 -e "MASTERKUBEIP=130.211.113.209" --name stormy_app -t huge/docker_stormy'

