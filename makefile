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

airflow:
	docker-compose -f docker-compose-airflow.yml up -d


airflow-stop:
	docker-compose -f docker-compose-airflow.yml stop

airflow-shutdown:
	docker-compose -f docker-compose-airflow.yml down

airflow-build:
	docker build -f Dockerfile-airflow --rm --build-arg PYTHON_DEPS="requests==2.22.0 pymongo==3.8.0 pillow==6.0.0 numpy==1.16.4 mongoengine==0.18.2" -t puckel/docker-airflow .
	docker image prune -f