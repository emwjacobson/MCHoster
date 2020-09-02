
up:
	docker-compose -f docker-compose-prod.yml up --build -d

up-dev:
	docker-compose -f docker-compose-dev.yml up --build

down:
	docker-compose -f docker-compose-prod.yml down --rmi all -v

down-dev:
	docker-compose -f docker-compose-dev.yml down --rmi all -v

setup:
	docker build --pull --rm -t mcserver:latest mcserver
