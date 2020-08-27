IMAGE_NAME=mchoster-server

all: build run

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it -p 25565:25565 -v test_srv:/server $(IMAGE_NAME):latest