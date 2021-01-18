username = emwjacobson

# up:
# 	docker-compose -f docker-compose-prod.yml up --build -d

# up-dev:
# 	docker-compose -f docker-compose-dev.yml up --build

# down:
# 	docker-compose -f docker-compose-prod.yml down --rmi all

# down-dev:
# 	docker-compose -f docker-compose-dev.yml down --rmi all

build:
	docker login
	docker build -t $(username)/mchoster_manager:latest manager
	docker build -t $(username)/mchoster_nginx:latest nginx
	docker build -t $(username)/mchoster_web:latest web
	docker push $(username)/mchoster_manager
	docker push $(username)/mchoster_nginx
	docker push $(username)/mchoster_web

deploy-server:
	docker login
	docker build --pull --rm -t mcserver:latest mcserver
	docker tag mcserver:latest $(username)/mcserver:latest
	docker push $(username)/mcserver:latest
