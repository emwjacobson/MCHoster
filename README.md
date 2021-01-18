
# MCHoster

## About

The goal of this project was to make an on demand Minecraft server hosting website where users would be able to spin up servers whenever they wanted.

I wanted to get more experience using tools like Docker and Django. This lead to the decision to use Docker containers for running the servers, backend, and web server, as well as using Django as the framework for the web server.

From the start of the project I had the idea of being able to incorporate Docker Swarm or Kubernetes in order to scale the project if more servers were needed. I was finally able to accomplish this in "v2" of the project. I used Docker Swarm in order to distribute the workload across multiple nodes, as well as introducing some High Availability into the project.

## Components

### manager
This is the manager that handles the creation and destruction of the MC servers. It communicates with the web server using HTTP requests.

### mcserver
This is the image of the MC server itself. It uses [PaperMC](https://papermc.io/) which is a high-performance fork of Spigot.

### web
This is a Django web server, it handles the interactions with the end users and communicates with the manager.

## Requirements

### Software
- build-essential
- A [Gluster](https://www.gluster.org/) share (production only)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Hardware

- ~1 core & ~1.5gb of ram __per Minecraft server__ you want to be able to host.

## Running (Production)

### Setup Gluster

Because there is shared data between `web` and the `nginx` service, there must be shared data across all servers you want running in the Swarm. To accomplish this, create a GlusterFS share and use a [glusterfs volume plugin](https://github.com/marcelo-ochoa/docker-volume-plugins/tree/master/glusterfs-volume-plugin) for docker in order to mount the share in containers.

A tutorial for setting up a Gluster share is located [here](https://medium.com/running-a-software-factory/setup-3-node-high-availability-cluster-with-glusterfs-and-docker-swarm-b4ff80c6b5c3), though any will really do.

**Note**: At the time of writing this, the LTS version of gluster is **7**. The tutorial above uses version **6**. Because of this, in step 3 `add-apt-repository ppa:gluster/glusterfs-6` should be replaced with `add-apt-repository ppa:gluster/glusterfs-7`. If 7 is not the LTS at the time of reading, please adjust accordingly.

**Note**: The volume name used in this is `docker_gfs`. If you wish to change this, the `name` will also need to be updated in the `volume` section of the `docker-compose.yml` file.

**Note**: For the glusterfs volume plugin, `PLUGINALIAS` was replaced with `glusterfs`. If you decide to use a different name, the `driver` name will also need to be updated in the `volume` section of the `docker-compose.yml` file.

### Creating the Docker swarm

You can learn about how to create a Docker swarm [in their tutorials](https://docs.docker.com/engine/swarm/). For MCHoster, you need at least one manager node and any number of workers. You can run the entire stack on a single manager node if you wish.

The only service that needs to be on a manager node is the `manager` service, as it interacts with the swarm itself. Therefore it needs a manager role.

### Running MCHoster

The full repository does not need to be cloned to run in production, instead the `docker-compose.yml` file can be downloaded.
```
curl https://raw.githubusercontent.com/emwjacobson/MCHoster/master/docker-compose.yml -o docker-compose.yml
```

**The following information will need to be changed in the `docker-compose.yml` file in order to have things run correctly**:
Under the `web` service, `SERVER_IP` should be set to the IP that the users should use to connect to the Minecraft server. `SECRET_KEY` should be set to a long, random string. `SECRET_KEY` is used by Django, and this key should **not** be shared. `ALLOWED_HOSTS` should be set to one or more (comma separated) hosts that are allowed to access MCHoster.

After the changes have been made, you can use `docker stack deploy` to have all of the services created across the swarm.

```
docker stack deploy --compose-file docker-compose.yml mchoster
```

**Note**: The stack is named `mchoster` as shown in the above command. If you wish to use a different stack name, it will need to be updated under the `manager` service in the `docker-compose.yml` file.

After the services are done being created, you should be able to access MCHoster using the IP of any node in the Swarm.


## Running (Development)

**Note**: A GlusterFS cluster is not required for development as there is no data shared between containers.

**Note**: Development should be done in a swarm consisting of **one** manager and any number of workers. All of the core services will be assigned to that manager. There are local directories that need to be mounted to make sure that files are updated inside of the containers. Development should be done on the manager node so files are mounted correctly.

Clone the repo on the manager node.
```
git clone https://github.com/emwjacobson/MCHoster
```

Update the variables in the `docker-compose-dev.yml` files, similarly to how they should be updated in the production section. The variables that should be updated are `SERVER_IP` and `SECRET_KEY`.

You can then deploy the stack.

```
docker stack deploy --compose-file docker-compose-dev.yml
```

**Note**: All core containers should be running on the single manager node.

Development can now be done directly on `manager` and `web`. Because their respective directories are mounted in the containers, the default container files are overwritten, allowing you to make live edits.

Once edits are done, you can build, tag, and push the images to Docker Hub. To use images other than the defaults, the images will needed to be updated in the `docker-compose*.yml` files.
