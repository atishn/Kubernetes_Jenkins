###Info
The kubernetes master server ('kubernetes-master') has a built in API as described here: . It can be accessed via the public ip for the master server. For example https://130.211.122.34/api/v1beta1/replicationControllers will list the current ReplicationControllers. Port 8080 must be opened for that server in GCE. The username and password needed to access the server can be found in the ~/.kubernetes_auth file on your machine (assuming that you followed the directions in 'Setup Kubernetes cluster on local machine').

We have created this simple flask app that utilizes that api as a POC. The longterm plan is to have these api calls be fired automatically to resize the jenkins slaves based on usage using Celery.

###Run the app:
Download the repo and run:

			(sudo) pip install Flask
			(sudo) pip install flask-restful
			(sudo) pip install requests
			python stormy_app.py

###List Pods
Visit http://localhost:5000/pods to see a json list of the current pods
Visit http://localhost:5000/pods/<pod_id> to see info for a specific pod
List Replication Controllers
Visit http://localhost:5000/replicationControllers to see a json list of the current replication controllers
Visit http://localhost:5000/replicationControllers/<replication_controller_id> to see info for a specific replication controller

###List Services
Visit http://localhost:5000/services to see a json list of the current pods
Visit http://localhost:5000/sevices/<service_id> to see info for a specific pod

###New Replication Controller
Visit http://localhost:5000/new/replicationController?name=<name>&image=<docker_image_name>&num=<num_pods>. For example: http://localhost:5000/new/replicationController?name=jenkinsmaster&image=jenkins_pipeline&num=2. Name must be lowercase and will be used for the id, labels and container names.
	
###Resize Replication Controller
Visit http://localhost:5000/resize?id=<controller_name>&num=<new_size>. For example http://localhost:5000/resize?id=jenkinsMasterController&num=0. Will return a json of the current state and the requested state. (Will only work if you have already created a ReplicationController with that id).
