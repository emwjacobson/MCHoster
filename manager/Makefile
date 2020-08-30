IMAGE_NAME=mchoster-manager

all: build

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it --net mcsm --network-alias manager -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE_NAME):latest

dev:
	docker run --rm -it --net mcsm --network-alias manager -p 8080:80 -v /var/run/docker.sock:/var/run/docker.sock -v $(shell pwd):/manager $(IMAGE_NAME):latest flask run -h 0.0.0.0 -p 80 --debugger --reload
