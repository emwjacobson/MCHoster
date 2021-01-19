username = emwjacobson

# up:
# 	docker-compose -f docker-compose-prod.yml up --build -d

# up-dev:
# 	docker-compose -f docker-compose-dev.yml up --build

# down:
# 	docker-compose -f docker-compose-prod.yml down --rmi all

# down-dev:
# 	docker-compose -f docker-compose-dev.yml down --rmi all

deploy-all:
	docker login
	docker build -t $(username)/mchoster_manager:latest manager
	docker build -t $(username)/mchoster_nginx:latest nginx
	docker build -t $(username)/mchoster_web:latest web
	docker build -t $(username)/mcserver:latest mcserver
	docker push $(username)/mchoster_manager:latest
	docker push $(username)/mchoster_nginx:latest
	docker push $(username)/mchoster_web:latest
	docker push $(username)/mcserver:latest
