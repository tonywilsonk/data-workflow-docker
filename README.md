# data-workflow-docker
An implementation of an asynchronous data workflow with docker using python3, flask, docker, celery, mongodb

The purpose is to implement a simple workflow to process image file asynchronously.
The workflow is divided in 3 steps:
1. extract: download image 
2. transform: apply various operations on the image
3. load: load image matadata in mongodb 

The application uses celery to make all the stuf. We use Redis as how broker and flower to monitor celery tasks.

For the application purposes, we also build a flask api to visualize images store in mongo db and also retrieve statistics about execution errors.

## A solution with Apache Airflow

Apache Airflow is a great tool. The main idea behind the solution with airflow is to buid a dynamic worflow based on the number of images to process. The main task () create for each image to process a subtack, ETL to do.

![Main Task](https://github.com/tonywilsonk/data-workflow-docker/blob/master/big.PNG)

The main task(Workflow)

![Etl Task](https://github.com/tonywilsonk/data-workflow-docker/blob/master/etl.PNG)

The subtask Workflow (ETL)

![After Running](https://github.com/tonywilsonk/data-workflow-docker/blob/master/success.PNG)

All done with success :) .

Refer to makefile for how to run the solution with airflow. We are able to access to airflow at http://localhost:8080 and run the DAG.

## How to run all this stuf

using make, all become more simple :).
In the top directory of the project, run the following commands:

1. make build

  this build all docker images we need

2. make run

  Run docker compose with all need services and also create a share volume for all celery workers to pass temporary files
  After this, we can go to **http://localhost:8081** to view mongo-express, **http://localhost:5555** to view flower and **http://localhost:5000** for flask api.
  
3. docker exec -it < container name of service workflow > python3 workflow.py
  
  This command runs the workflow for processing of all the urls in urls.txt file. After this, we successfully process 650 urls from  urls.py file.
  

## Stop and shutdown

we can use make also to stop or shutdown all docker containers. Refer to the makefile of the project.
