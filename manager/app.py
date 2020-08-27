import docker
from flask import *
from mcstatus import MinecraftServer

app = Flask(__name__)
client = docker.from_env()

success = {"status": "success"}
error = {"status": "error"}

check_label = "mcsm"

server_limit = 15

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

def get_containers():
    """Returns list of containers running MC Server

    Returns:
        List: List of Containers, sorted from newest to oldest. list[0] is newest, list[-1] is oldest
    """
    return sorted(client.containers.list(filters={"label": [check_label]}), key=lambda x: x.attrs['Created'], reverse=True)

def create_container(username):
    """Created a new server container

    Args:
        username (string): The username for the OP user (unimplemented)

    Returns:
        Container: The mc server container
    """
    vol = {username: {'bind': '/server', 'mode': 'rw'}} if username != None else False
    return client.containers.run('mchoster-server', mem_limit='1.5g', cpu_quota=100000, cpu_period= 100000,
                                 remove=True, detach=True, ports={'25565/tcp': None, '25565/udp': None},
                                 labels={check_label: '', 'username': username}, network=check_label,
                                 volumes=vol)


@app.route('/stats')
def stats():
    try:
        containers = get_containers()
        return {
            **success,
            "message": "",
            "num_running": len(containers),
            "servers": [{
                "id": c.id,
                "port": get_port(c),
                "created": c.attrs['Created']
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
            "created": container.attrs['Created']
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

    try:
        containers = get_containers()
        if len(containers) >= server_limit:
            return {
                **error,
                "message": "Maximum amount of servers reached"
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
            container.exec_run("/bin/sh -c 'kill $(pidof java)'", detach=True)
            container.stop(timeout=30)
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


@app.route('/')
def index():
    return "", 404

if __name__ == "__main__":
    for c in get_containers():
        try:
            server = MinecraftServer.lookup(get_ip(c))
            print(server.status().players.online)
        except ConnectionRefusedError as e:
            print(f"Server {get_ip(c)} down?")
