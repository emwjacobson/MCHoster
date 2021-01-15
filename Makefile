username = emwjacobson

# up:
# 	docker-compose -f docker-compose-prod.yml up --build -d

# up-dev:
# 	docker-compose -f docker-compose-dev.yml up --build

# down:
# 	docker-compose -f docker-compose-prod.yml down --rmi all

# down-dev:
# 	docker-compose -f docker-compose-dev.yml down --rmi all

deploy-server:
	docker login
	docker build --pull --rm -t mcserver:latest mcserver
	docker tag mcserver:latest $(username)/mcserver:latest
	docker push $(username)/mcserver:latest
