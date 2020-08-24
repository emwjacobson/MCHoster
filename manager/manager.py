import docker
from flask import *

app = Flask(__name__)
client = docker.from_env()

@app.route('/stats')
def stats():
    return {'containers_running': len(client.containers.list(filters={"label": ['mcsm']}))}

@app.route('/start_server')
def start_server():
    # TODO: Set container
    # client.containers.run('', detach=True, labels=['mcsm'])
    return 'TODO'

@app.route('/')
def index():
    return 'Home'

if __name__ == "__main__":
    app.run()