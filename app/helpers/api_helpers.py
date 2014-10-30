from flask import current_app as app

import json
import requests

def new_replication_controller(name, num, image):
    
    req_obj = {
        "id": name + 'Controller',
        "apiVersion": "v1beta1",
        "kind": "ReplicationController",
        "desiredState": {
          "replicas": num,
          "replicaSelector": {"name": name},
          "podTemplate": {
            "desiredState": {
               "manifest": {
                 "version": "v1beta1",
                 "id": name + "Controller",
                 "containers": [{
                   "name": name,
                   "image": app.config['DOCKER_REGISTRY'] + '/' + image,
                   "ports": [{"containerPort": 8080, "hostPort": 49162}]
                 }]
               }
             },
             "labels": {"name": name}
            }},
        "labels": {"name": name}
      }


    req_json = json.dumps(req_obj)


    url = 'https://{0}/api/v1beta1/replicationControllers'.format(app.config['MASTER_IP'])

    print req_json

    r = requests.post(url, data=req_json, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return r.json()

def resize_replication_controller(controller_id, num):
    controller_url = 'https://{0}/api/v1beta1/replicationControllers/{1}'.format(app.config['MASTER_IP'], controller_id)

    request_controller = requests.get(controller_url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    current_controller =  request_controller.json()

    if current_controller['kind'] == "Status":
        return current_controller

    current_controller['desiredState']['replicas'] = num

    # need to dump to get rid of unicode u'
    new_controller = json.dumps(current_controller)

    put_response = requests.put(controller_url, data=new_controller, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return put_response.json()

def get_replication_size(controller_id):
    controller_url = 'https://{0}/api/v1beta1/replicationControllers/{1}'.format(app.config['MASTER_IP'], controller_id)

    controller = requests.get(controller_url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    controller_json =  controller.json()

    if controller_json['kind'] == "Status":
        return False

    return controller_json['desiredState']['replicas']