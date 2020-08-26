IMAGE_NAME=mchoster-manager

all: build

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it -p 8080:5000 -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE_NAME):latest
