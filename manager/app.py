import docker
from flask import *

app = Flask(__name__)
client = docker.from_env()

success = {"status": "success"}
error = {"status": "error"}

def get_port(container):
    return container.attrs['NetworkSettings']['Ports']['25565/tcp'][0]['HostPort']

@app.route('/stats')
def stats():
    try:
        containers = client.containers.list(filters={"label": ["mcsm"]})
        return {
            **success,
            "message": "",
            "num_running": len(containers),
            "ids": [c.id for c in containers]
        }
    except docker.errors.APIError as e:
        return {
            **error,
            "message": "Docker API Error"
        }
    except Exception as e:
        return {
            **error,
            "message": "An error has occured"
        }


@app.route('/stats/<cid>')
def stats_container(cid):
    cid = escape(cid)
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
            "message": "Container not found"
        }
    except Exception as e:
        return {
            **error,
            "message": "An error has occured"
        }

@app.route('/start')
@app.route('/start/<username>')
def start_server(username=None):
    try:
        container = client.containers.run('mchoster-server', mem_limit='2g', cpu_count=2, remove=True, detach=True, ports={'25565/tcp': None, '25565/udp': None}, labels=['mcsm'])
    except docker.errors.ImageNotFound as e:
        return {
            **error,
            "message": "Container image not found"
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
    try:
        container = client.containers.get(cid)
        container.stop(timeout=10)
        return {
            **success,
            "message": "Container stopped"
        }
    except docker.errors.NotFound as e:
        return {
            **error,
            "message": f"Container {cid} does not exist"
        }


@app.route('/')
def index():
    return "", 404

if __name__ == "__main__":
    app.run()