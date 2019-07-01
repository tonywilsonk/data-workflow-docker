# encoding: utf-8

import os
from mongoengine import *

MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'workflowdb')
MONGO_USERNAME = os.getenv('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'breacmpa')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')


connect(MONGO_DATABASE, host=MONGO_HOST, port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD, authentication_source='admin')