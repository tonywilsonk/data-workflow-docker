#!make

build:
	docker build -f Dockerfile-flask -t workflow-flask .
	docker build -f Dockerfile-worker -t workflow-worker .
	docker image prune -f

run:
	docker volume create data-volume
	docker-compose up -d

stop:
	docker-compose stop

shutdown:
	docker-compose down
	docker volume rm data-volume

