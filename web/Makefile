IMAGE_NAME=mchoster-web

all: build

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it --net mcsm -p 8888:8000 $(IMAGE_NAME):latest

dev:
	docker run --rm -it --net mcsm -p 8888:5000 -v $(shell pwd):/app $(IMAGE_NAME):latest bash
