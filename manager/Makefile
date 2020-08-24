
all: build

build:
	docker build --pull --rm -t mchoster-manager:latest .

run:
	docker run --rm -it -p 8080:5000 -v /var/run/docker.sock:/var/run/docker.sock mchoster-manager:latest