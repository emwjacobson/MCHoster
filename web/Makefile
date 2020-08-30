IMAGE_NAME=mchoster-web

all: build

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it --net mcsm --network-alias web -p 8888:80 $(IMAGE_NAME):latest

dev:
	docker run --rm -it --net mcsm --network-alias web -p 8888:80 -v $(shell pwd):/app $(IMAGE_NAME):latest python manage.py runserver 0:80
