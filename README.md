# MCHoster

## About
The goal of this project was to make an on demand minecraft server hosting website where users would be able to spin up servers on command.

I wanted to get more experience in tools like Docker and Django, which is why I am using Docker containers for running the servers, backend, and web server, and Django as the framework for the web server.

## Components

### manager
This is the manager that handles the creation and destruction of the MC servers. It communicates with the web server using a REST api.

### mcserver
This is the image of the MC server itself. It is based off [PaperMC](https://papermc.io/) which claims to be a high-performance fork of Spigot.

### web
This is the Django web server, it handles the interactions with the end users.

### db
This will be the container that manages the databases. Still unimplemented.

## Requirements
### Software
- Docker

### Hardware
- ~1 core & ~1.5gb of ram per server you want to be able to host

## Running
Things are still changing quickly. This will be updated with instructions once things become more stable.
