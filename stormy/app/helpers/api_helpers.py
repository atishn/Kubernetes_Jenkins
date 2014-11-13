import json

from flask import current_app as app
import httplib
import requests


def new_replication_controller(name, controller_id, num, image, ports=[], variables=None):
    ports_json = bulid_ports_json(ports)
    env_json = build_env_json(variables)

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
                        "id": controller_id,
                        "containers": [{
                                           "name": name,
                                           "image": app.config['DOCKER_REGISTRY'] + '/' + image,
                                           "ports": ports_json,
                                           "env": env_json
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


def resize_replication_controller(name, controller_id, num, image, ports=[], variables=None):
    controller_url = 'https://{0}/api/v1beta1/replicationControllers/{1}'.format(app.config['MASTER_IP'], controller_id)

    request_controller = requests.get(controller_url, auth=(app.config['API_USER'], app.config['API_PASS']),
                                      verify=False)
    current_controller = request_controller.json()

    if current_controller['code'] == httplib.NOT_FOUND:
        response = new_replication_controller(name, controller_id, num, image, ports, variables)
    else:
        current_controller['desiredState']['replicas'] = num

        # need to dump to get rid of unicode u'
        new_controller = json.dumps(current_controller)

        response = requests.put(controller_url, data=new_controller,
                                    auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return response.json()


def get_replication_size(controller_id):
    controller_url = 'https://{0}/api/v1beta1/replicationControllers/{1}'.format(app.config['MASTER_IP'], controller_id)

    controller = requests.get(controller_url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    controller_json = controller.json()

    if controller_json['kind'] == "Status":
        return False

    return controller_json['desiredState']['replicas']


def new_pod(name, image, ports):
    ports_json = bulid_ports_json(ports)

    req_obj = {
        "id": name,
        "kind": "Pod",
        "apiVersion": "v1beta1",
        "desiredState": {
            "manifest": {
                "version": "v1beta1",
                "id": name,
                "containers": [
                    {
                        "name": name,
                        "image": app.config['DOCKER_REGISTRY'] + '/' + image,
                        "ports": ports_json
                    }
                ]
            }
        },
        "labels": {
            "name": name
        }
    }

    req_json = json.dumps(req_obj)

    url = 'https://{0}/api/v1beta1/pods'.format(app.config['MASTER_IP'])

    print req_json

    r = requests.post(url, data=req_json, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return r.json()


def list_objects(item_id):
    url = 'https://{0}/api/v1beta1/{1}'.format(app.config['MASTER_IP'], item_id)

    r = requests.get(url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return r.json()


def get_pod_byid(id):
    url = 'https://{0}/api/v1beta1/pods/{1}'.format(app.config['MASTER_IP'], id)
    r = requests.get(url, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return r.json()


def findHostPort(pod):
    hostIp = pod.get('currentState').get('hostIP')
    return hostIp


def findPodPort(pod):
    hostIp = pod.get('currentState').get('podIP')
    return hostIp


def new_service(name, serviceport, containerport, selectorkey, selectorvalue):
    req_obj = {
        "id": name,
        "kind": "Service",
        "apiVersion": "v1beta1",
        "protocol": "TCP",
        "port": serviceport,
        "containerPort": containerport,
        "selector": {
            selectorkey: selectorvalue
        }
    }

    req_json = json.dumps(req_obj)

    url = 'https://{0}/api/v1beta1/services'.format(app.config['MASTER_IP'])

    print req_json
    r = requests.post(url, data=req_json, auth=(app.config['API_USER'], app.config['API_PASS']), verify=False)
    return r.json()


def bulid_ports_json(ports):
    port_json = []

    for p in ports:
        json = {'containerPort': p[0], 'hostPort': p[1]}
        port_json.append(json)

    return port_json

def build_env_json(env):
    env_json = []

    for p in env:
        json = {'name': p[0], 'value': p[1]}
        env_json.append(json)
    return env_json
