# MCHoster

## Running


### **NOTE: Below documentation refers to v1 of the project. It has not yet been updated to reflect the changes in version 2.**

---


## About
The goal of this project was to make an on demand minecraft server hosting website where users would be able to spin up servers on command.

I wanted to get more experience in tools like Docker and Django, which is why I am using Docker containers for running the servers, backend, and web server, and using Django as the framework for the web server.

## Components

### manager
This is the manager that handles the creation and destruction of the MC servers. It communicates with the web server using a REST api.

### mcserver
This is the image of the MC server itself. It uses [PaperMC](https://papermc.io/) which is a high-performance fork of Spigot.

### web
This is a Django web server, it handles the interactions with the end users and communicates with the manager.

## Requirements
### Software
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- build-essential

### Hardware
- ~1 core & ~1.5gb of ram __per server__ you want to be able to host

## Running (Production)
- Build mcserver image
    - Can either be done using `make server` or `docker build --pull --rm -t mcserver:latest ./mcserver`
- Copy `docker-compose.yml` to `docker-compose-prod.yml` and edit settings
    - In `db` change:
        - `MYSQL_PASSWORD` to a new password
    - In `web` change:
        - `SERVER_IP` to the IP/URL of the server
        - `MYSQL_PASSWORD` to the same password as in `db`
        - `SECRET_KEY` to a __LONG random string__, used by Django
        - `ALLOWED_HOSTS` to the hosts allowed to connect to Django
- Run `make up` to bring up the docker-compose file
- To cleanup after, run `make down` to remove images

## Running (Development)
- Build mcserver image
    - Can either be done using `make server` or `docker build --pull --rm -t mcserver:latest ./mcserver`
- Edit `docker-compose-dev.yml` (Optional)
    - You can make the same modifications as in Running (Production)
    - The webserver will be available at :8888, and the manager at :8080
- Run `make up-dev` to bring up the development docker-compose file
- To cleanup after, run `make down-dev` to remove images
