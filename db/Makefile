IMAGE_NAME=mchoster-db

all: build

build:
	docker build --pull --rm -t $(IMAGE_NAME):latest .

run:
	docker run --rm -it --net mcsm --network-alias db -v db:/var/lib/mysql -e MYSQL_DATABASE=web -e MYSQL_USER=web -e MYSQL_PASSWORD=NotSoSecretPasswd -e MYSQL_RANDOM_ROOT_PASSWORD=yes $(IMAGE_NAME):latest

dev:
	docker run --rm -it --net mcsm --network-alias db -v db:/var/lib/mysql -e MYSQL_DATABASE=web -e MYSQL_USER=web -e MYSQL_PASSWORD=NotSoSecretPasswd -e MYSQL_RANDOM_ROOT_PASSWORD=yes $(IMAGE_NAME):latest bash
