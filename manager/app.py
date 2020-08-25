import docker
from flask import *

app = Flask(__name__)
client = docker.from_env()

success = {"status": "success"}
error = {"status": "error"}

server_limit = 10

def get_port(container):
    return container.attrs['NetworkSettings']['Ports']['25565/tcp'][0]['HostPort']

def get_containers():
    return client.containers.list(filters={"label": ["mcsm"]})

@app.route('/stats')
def stats():
    try:
        containers = get_containers()
        return {
            **success,
            "message": "",
            "num_running": len(containers),
            "servers": [{"id": c.id, "port": get_port(c)} for c in containers]
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
    if len(cid) < 20:
        return {
            **error,
            "message": "Invalid container"
        }

    try:
        container = client.containers.get(cid)

        return {
            **success,
            "message": "",
            "id": cid,
            "port": get_port(container)
        }
    except docker.errors.NotFound as e:
        return {
            **error,
            "message": e.explanation
        }
    except Exception as e:
        return {
            **error,
            "message": "An error has occured"
        }

@app.route('/start')
@app.route('/start/<username>')
def start_server(username=None):
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
        container = client.containers.run('mchoster-server', mem_limit='1.5g', cpu_quota=150000, remove=True,
                                          detach=True, ports={'25565/tcp': None, '25565/udp': None}, labels={'mcsm': '', 'username': username})
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
            c.exec_run("/bin/sh -c 'kill $(pidof java)'", detach=True)
        return {
            **success,
            "message": "Servers stopping"
        }

    try:
        container = client.containers.get(cid)
        if 'mscm' in container.labels:
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
    app.run()