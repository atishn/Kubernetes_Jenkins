{
    "id": "nginxController",
    "apiVersion": "v1beta1",
    "kind": "ReplicationController",
    "desiredState": {
      "replicas": 2,
      "replicaSelector": {"name": "nginx"},
      "podTemplate": {
        "desiredState": {
           "manifest": {
             "version": "v1beta1",
             "id": "nginxController",
             "containers": [{
               "name": "nginx",
               "image": "dockerfile/nginx",
               "ports": [{"containerPort": 80, "hostPort": 8080}]
             }]
           }
         },
         "labels": {"name": "nginx"}
        }},
    "labels": {"name": "nginx"}
  }


  args = {}
  json = {
    "id": args['name'] + 'Controller' ,
    "apiVersion": "v1beta1",
    "kind": "ReplicationController",
    "desiredState": {
      "replicas": 2,
      "replicaSelector": {"name": "nginx"},
      "podTemplate": {
        "desiredState": {
           "manifest": {
             "version": "v1beta1",
             "id": "nginxController",
             "containers": [{
               "name": "nginx",
               "image": "dockerfile/nginx",
               "ports": [{"containerPort": 80, "hostPort": 8080}]
             }]
           }
         },
         "labels": {"name": "nginx"}
        }},
    "labels": {"name": "nginx"}
  }