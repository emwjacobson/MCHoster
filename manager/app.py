import docker
from flask import *
from mcstatus import MinecraftServer
from datetime import datetime
import time

# Global Variables

app = Flask(__name__)
client = docker.from_env()

success = {"status": "success"}
error = {"status": "error"}

check_label = "mchoster_default"

server_limit = 10

min_age = 180

# END Global Variables


# Helper Functions

def get_port(container):
    """Returns the port that `container` is attached to on the host

    Args:
        container (Container): The mc server container

    Returns:
        int: The port that the mc server is attached to on the host
    """
    return int(container.attrs['NetworkSettings']['Ports']['25565/tcp'][0]['HostPort'])

def get_ip(container):
    """Returns the IP address of `container`

    Args:
        container (Container): The mc server container

    Returns:
        str: IP Address of the container
    """
    return container.attrs['NetworkSettings']['Networks'][check_label]['IPAddress']

def get_online(container):
    """Gets the number of players online on a server

    Args:
        container (Container): The container to check the amount of players

    Returns:
        int: The number of players on the server
    """
    # If the server is <3 minutes old, just return 0. Chances are its still being setup and checking a server thats still starting causes a slowdown
    if (datetime.now() - get_created(container)).total_seconds() < min_age:
        return 0
    try:
        server = MinecraftServer.lookup(get_ip(container))
        return server.status().players.online
    except Exception as e:
        return 0

def get_created(container) -> datetime:
    """Gets the datetime of when a container was created

    Args:
        container (Container): The container to find the time created of

    Returns:
        datetime: The datetime object of when the container was created
    """
    # Might be something like ISO 8601 to reduce the headache with this formatting
    pi = container.attrs['Created'].index(".")
    return datetime.strptime(container.attrs['Created'][0:pi], "%Y-%m-%dT%H:%M:%S")

def get_containers():
    """Returns list of containers running MC Server

    Returns:
        List: List of Containers, sorted from newest to oldest. list[0] is newest, list[-1] is oldest
    """
    return sorted(client.containers.list(filters={"label": [check_label]}), key=lambda x: get_created(x), reverse=True)

def create_container(username):
    """Created a new server container

    Args:
        username (string): The username for the OP user (unimplemented)

    Returns:
        Container: The mc server container
    """
    vol = {username: {'bind': '/server', 'mode': 'rw'}} if username != None else False
    env = [f"OP_USERNAME={username}"] if username != None else False
    return client.containers.run('mcserver:latest', mem_limit='1.5g', cpu_quota=100000, cpu_period= 100000,
                                 remove=True, detach=True, ports={'25565/tcp': None, '25565/udp': None},
                                 labels={check_label: '', 'username': username}, network=check_label,
                                 volumes=vol, environment=env)

def stop_container(container):
    """Stops `container`

    Args:
        container (Container): The container you want to stop
    """
    container.exec_run("/bin/sh -c 'kill $(pidof java)'", detach=True)
    container.stop(timeout=30)

# END Helper Functions


# REST Endpoints

@app.route('/stats')
def stats():
    try:
        containers = get_containers()

        return {
            **success,
            "message": "",
            "num_running": len(containers),
            "max_running": server_limit,
            "servers": [{
                "id": c.id,
                "port": get_port(c),
                "created": get_created(c),
                "alive_for": (datetime.now() - get_created(c)).total_seconds(),
                "num_players": get_online(c),
                "username": c.labels['username']
            } for c in containers]
        }
    except docker.errors.APIError as e:
        return {
            **error,
            "message": e.explanation
        }
    except Exception as e:
        print(e)
        return {
            **error,
            "message": "An error has occured"
        }

@app.route('/stats/<cid>')
def stats_container(cid):
    cid = escape(cid)
    if len(cid) < 64:
        return {
            **error,
            "message": "Invalid container id"
        }

    try:
        container = client.containers.get(cid)

        return {
            **success,
            "message": "",
            "id": cid,
            "port": get_port(container),
            "created": get_created(container),
            "alive_for": (datetime.now() - get_created(container)).total_seconds(),
            "num_players": get_online(container),
            "username": container.labels['username']
        }
    except docker.errors.NotFound as e:
        return {
            **error,
            "message": e.explanation
        }
    except Exception as e:
        print(e)
        return {
            **error,
            "message": "An error has occured"
        }

@app.route('/start')
@app.route('/start/<username>')
def start_server(username=None):
    if username != None:
        username = escape(username)
        if len(username) < 5:
            return {
                **error,
                "message": "Username too short"
            }

    try:
        containers = get_containers()
        if len(containers) >= server_limit:
            return {
                **error,
                "message": "Maximum amount of servers reached"
            }

        for c in containers:
            if c.labels['username'] == username:
                return {
                    **error,
                    "message": "A server with that username has already been started"
                }
    except docker.errors.APIError as e:
        return {
            **error,
            "message": e.explanation
        }

    try:
        container = create_container(username)
    except docker.errors.ImageNotFound as e:
        return {
            **error,
            "message": e.explanation
        }

    try:
        container.reload()
        return {
            **success,
            "message": "Container started",
            "id": container.id,
            "port": get_port(container)
        }
    except Exception as e:
        print(e)
        container.stop()
        return {
            **error,
            "message": "An error has occured"
        }

@app.route('/stop/<cid>')
def stop_server(cid):
    cid = escape(cid)

    # TODO: Remove this in the future
    if cid == 'all':
        for c in get_containers():
            stop_server(c.id)
        return {
            **success,
            "message": "Servers stopping"
        }

    if len(cid) < 64:
        return {
            **error,
            "message": "Invalid container"
        }

    try:
        container = client.containers.get(cid)
        if check_label in container.labels:
            if (datetime.now() - get_created(container)).total_seconds() < min_age:
                return {
                    **error,
                    "message": "Container is too new to be stopped"
                }
            stop_container(container)
            return {
                **success,
                "message": "Container stopped"
            }
        else:
            raise docker.errors.NotFound("", explanation=f"No such container: {cid}")
    except docker.errors.NotFound as e:
        return {
            **error,
            "message": e.explanation
        }

@app.route('/reset/<username>')
def reset_server(username):
    if username != None:
        username = escape(username)
        if len(username) < 5:
            return {
                **error,
                "message": "Username too short"
            }

    # Stop any servers with the username if they are running
    for c in get_containers():
        if c.labels['username'] == username:
            stop_container(c)
            break

    # Make sure the volume for `username` exists
    try:
        vol = client.volumes.get(username)
    except docker.errors.NotFound as e:
        return {
            **error,
            "message": "Username not found"
        }
    except Exception as e:
        print(e)
        return {
            **error,
            "message": "There was an error"
        }

    # Finally remove the volume
    try:
        vol.reload()
        vol.remove(force=True)
    except Exception as e:
        print(e)
        return {
            **error,
            "message": "There was an error"
        }

    return {
        **success,
        "message": "Server has been reset"
    }

@app.route('/')
def index():
    return "", 404

# END REST Endpoints


# This code is ran when the program is run as pure python.
# Intended to be used as a cron-job to clean up servers

if __name__ == "__main__":

    for c in get_containers():
        diff = datetime.now() - get_created(c)
        total_seconds = diff.total_seconds()
        if (total_seconds > 600):
            try:
                num_online = get_online(c)

                if num_online == 0:
                    print("Stopping container for being alive too long without active players")
                    stop_container(c)
            except ConnectionRefusedError as e:
                print(f"Server {get_ip(c)} down?")
