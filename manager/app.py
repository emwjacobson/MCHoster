import time
import os
import socket
from datetime import datetime
import docker
from docker.models.services import Service
from docker.types import Resources, EndpointSpec
from flask import Flask, escape
from mcstatus import MinecraftServer

###################################
#
# Global Variables
#
###################################


app = Flask(__name__)
client = docker.from_env()
client.networks.prune()

response_success = {"status": "success"}
response_error = {"status": "error"}

stack_name = os.environ.get('STACK_NAME')

# server_limit = int(os.environ.get('MAX_SERVERS')) if os.environ.get('MAX_SERVERS') is not None else 10
server_per_node = 3

min_age = 60

port_min = 30000
port_max = 32000
port_last = port_min

# server_prefix = "serverfiles_"

###################################
#
# END Global Variables
#
###################################











###################################
#
# Helper Functions
#
###################################

def get_port(service: Service):
    """Returns the port that `service` is attached to on the host

    Args:
        service (Service): The mc server service

    Returns:
        int: The port that the mc server is attached to on the host
    """
    print(service.attrs)
    return int(service.attrs['Endpoint']['Ports'][0]['PublishedPort'])

# def get_ip(service: Service):
#     """Returns the IP address of `service`

#     Args:
#         service (Service): The mc server service

#     Returns:
#         str: IP Address of the service
#     """
#     return service.attrs['NetworkSettings']['Networks'][check_label]['IPAddress']

def get_online(service: Service):
    """Gets the number of players online on a server

    Args:
        service (Service): The service to check the amount of players

    Returns:
        int: The number of players on the server
    """
    # If the server is <3 minutes old, just return 0. Chances are its still being setup and checking a server thats still starting causes a slowdown
    if (datetime.now() - get_created(service)).total_seconds() < min_age:
        return -1
    try:
        service.reload()
        ip = service.name + ":25565"
        print(ip)
        server = MinecraftServer.lookup(ip)
        return server.status().players.online
    except Exception as e:
        print(e)
        return -2

def get_created(service: Service) -> datetime:
    """Gets the datetime of when a service was created

    Args:
        service (Service): The service to find the time created of

    Returns:
        datetime: The datetime object of when the service was created
    """
    # Might be something like ISO 8601 to reduce the headache with this formatting
    createdAt = service.attrs['CreatedAt']
    pi = createdAt.index(".")
    return datetime.strptime(createdAt[0:pi], "%Y-%m-%dT%H:%M:%S")

# def get_created_volume(volume) -> datetime:
#     # Might be something like ISO 8601 to reduce the headache with this formatting
#     return datetime.strptime(volume.attrs['CreatedAt'], "%Y-%m-%dT%H:%M:%SZ")

def get_services():
    """Returns list of services running MC Servers

    Returns:
        List: List of Services
    """
    return client.services.list(filters={"label": [stack_name]})
    # return sorted(client.services.list(filters={"label": [check_label]}), key=lambda x: get_created(x), reverse=True)

def get_nodes():
    """Returns a list of nodes in the swarm

    Returns:
        List: List of Nodes
    """
    return client.nodes.list()

resources = Resources(mem_limit='1.5g')

def create_service(username):
    """Created a new server service

    Args:
        username (string): The username for the OP user

    Returns:
        Service: The mc server service
    """
    global port_last

    # vol = {check_label+"_user_"+username: {'bind': '/server', 'mode': 'rw'}} if username != None else False
    env = [f"OP_USERNAME={username}"] if username != None else [f"OP_USERNAME="]
    port_last = port_last + 1
    if port_last > port_max:
        port_last = port_min

    return client.services.create('emwjacobson/mcserver:latest', endpoint_spec=EndpointSpec(ports={port_last: (25565, "tcp")}),
                                 labels={stack_name: '', 'username': username}, env=env, networks=[stack_name+"_default"])
    # return client.containers.run('emwjacobson/mcserver:latest', mem_limit='1.5g', cpu_quota=100000, cpu_period=100000,
    #                              remove=True, detach=True, ports={'25565/tcp': port_range, '25565/udp': port_range},
    #                              labels={check_label: '', 'username': username}, network=check_label,
    #                              volumes=vol, environment=env)

def stop_service(service: Service):
    """Stops service `service`

    Args:
        service (Service): The service you want to stop
    """
    # service.exec_run("/bin/sh -c 'kill $(pidof java)'", detach=True)
    service.remove()


###################################
#
# END Helper Functions
#
###################################







###################################
#
# REST Endpoints
#
###################################


@app.route('/stats/')
def stats():
    try:
        services = get_services()
        nodes = get_nodes()

        rtn = {
            **response_success,
            "message": "",
            "num_nodes": len(nodes),
            "num_running": len(services),
            "servers": []
        }

        for service in services:
            created = get_created(service)
            rtn['servers'].append({
                "id": service.id,
                "port": get_port(service),
                "created": created,
                "alive_for": (datetime.now() - created).total_seconds(),
                "num_players": get_online(service),
                "username": service.attrs['Spec']['Labels']['username']
            })

        return rtn
    except docker.errors.APIError as e:
        return {
            **response_error,
            "message": e.explanation
        }
    except Exception as e:
        print(e)
        return {
            **response_error,
            "message": "an error has occured"
        }

@app.route('/stats/<cid>') # TODO
def stats_service(cid):
    return
    # cid = escape(cid)
    # if len(cid) < 64:
    #     return {
    #         **error,
    #         "message": "Invalid server id"
    #     }

    # try:
    #     container = client.containers.get(cid)

    #     return {
    #         **success,
    #         "message": "",
    #         "id": cid,
    #         "port": get_port(container),
    #         "created": get_created(container),
    #         "alive_for": (datetime.now() - get_created(container)).total_seconds(),
    #         "num_players": get_online(container),
    #         "username": container.labels['username']
    #     }
    # except docker.errors.NotFound as e:
    #     return {
    #         **error,
    #         "message": e.explanation
    #     }
    # except Exception as e:
    #     print(e)
    #     return {
    #         **error,
    #         "message": "An error has occured"
    #     }

@app.route('/start/')
@app.route('/start/<username>')
def start_server(username=None):
    services = sorted(get_services(), key=lambda x : get_created(x), reverse=True)

    if len(services) > 0:
        newest = services[0]
        diff = datetime.now() - get_created(newest)
        # If newest server was made less than 60 seconds ago, wait a bit before starting a new one
        if diff.total_seconds() < 60:
            return {
                **response_error,
                "message": f"Another server was created too recently. Please wait {60-diff.total_seconds():.0f} more seconds and try again."
            }

    if username != None:
        username = escape(username)
        if len(username) < 3:
            return {
                **response_error,
                "message": "Username too short"
            }

        if username.startswith(stack_name):
            return {
                **response_error,
                "message": f"Username cannot start with {stack_name}"
            }

    try:
        services = get_services()
        if len(services) >= server_per_node * len(get_nodes()):
            return {
                **response_error,
                "message": "Maximum amount of servers reached"
            }

        for service in services:
            if service.attrs['Spec']['Labels']['username'] == username:
                return {
                    **response_error,
                    "message": "A server with that username has already been started"
                }
    except docker.errors.APIError as e:
        return {
            **response_error,
            "message": e.explanation
        }

    try:
        service = create_service(username)
    except docker.errors.ImageNotFound as e:
        return {
            **response_error,
            "message": e.explanation
        }
    except docker.errors.APIError as e:
        return {
            **response_error,
            "message": "Error, please try again. Port might already be in use."
        }

    try:
        service.reload()
        return {
            **response_success,
            "message": "Server started",
            "id": service.id,
            "port": get_port(service)
        }
    except Exception as e:
        print(e)
        service.remove()
        return {
            **response_error,
            "message": "An error has occured"
        }

@app.route('/stop/<service_id>') # TODO
def stop_server(service_id):
    service_id = escape(service_id)

    if len(service_id) < 25:
        return {
            **response_error,
            "message": "Invalid server ID"
        }

    try:
        service = client.services.get(service_id)
        if stack_name in service.attrs['Spec']['Labels']:
            if (datetime.now() - get_created(service)).total_seconds() < min_age:
                return {
                    **response_error,
                    "message": "Server is too new to be stopped, please wait at least 3 minutes after starting"
                }
            stop_service(service)
            return {
                **response_success,
                "message": "Server stopped"
            }
        else:
            raise docker.errors.NotFound("", explanation=f"No such server: {service_id}")
    except docker.errors.NotFound as e:
        return {
            **response_error,
            "message": e.explanation
        }

@app.route('/reset/<username>') # TODO
def reset_server(username):
    return
    # if username != None:
    #     username = escape(username)
    #     if len(username) < 5:
    #         return {
    #             **error,
    #             "message": "Username too short"
    #         }

    # # Stop any servers with the username if they are running
    # for c in get_containers():
    #     if c.labels['username'] == username:
    #         stop_container(c)
    #         break

    # # Make sure the volume for `username` exists
    # try:
    #     vol = client.volumes.get(username)
    # except docker.errors.NotFound as e:
    #     return {
    #         **error,
    #         "message": "Username not found"
    #     }
    # except Exception as e:
    #     print(e)
    #     return {
    #         **error,
    #         "message": "There was an error"
    #     }

    # # Finally remove the volume
    # try:
    #     vol.reload()
    #     vol.remove(force=True)
    # except Exception as e:
    #     print(e)
    #     return {
    #         **error,
    #         "message": "There was an error"
    #     }

    # return {
    #     **success,
    #     "message": "Server has been reset"
    # }

@app.route('/')
def index():
    return "", 404


###################################
#
# END REST Endpoints
#
###################################














# This code is ran when the program is run as pure python.
# Intended to be used as a cron-job to clean up servers

if __name__ == "__main__":
    for service in get_services():
        diff = datetime.now() - get_created(service)
        total_seconds = diff.total_seconds()
        if total_seconds > 600:
            try:
                num_online = get_online(service)

                if num_online == 0:
                    print("Stopping server for being alive too long without active players")
                    stop_service(service)
            except ConnectionRefusedError as e:
                print(f"Server {service.name} down?")
