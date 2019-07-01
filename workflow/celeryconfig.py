# encoding: utf-8
from kombu import Queue


content_encoding = 'utf-8'
timezone = "europe/rome"
broker_url = "redis://redis:6379"
result_backend = "redis://redis:6379"
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
broker_pool_limit = 120
# celery queues setup
task_default_queue = 'extract'
task_default_routing_key = 'workflow.extract'

worker_enable_remote_control = False
worker_send_task_events = False

task_queues = (
    Queue('extract', routing_key='workflow.extract'),
    Queue('transform', routing_key='workflow.transform'),
    Queue('load', routing_key='workflow.load')
)

# celery queue routing
task_routes = {
    'workflow.tasks.download_file': {
        'queue': 'extract',
        'routing_key': 'workflow.extract',
    },
    'workflow.tasks.image_to_gray': {
        'queue': 'transform',
        'routing_key': 'workflow.transform',
    },
    'workflow.tasks.image_to_md5': {
        'queue': 'transform',
        'routing_key': 'workflow.transform',
    },
    'workflow.tasks.save_image_metadata': {
        'queue': 'load',
        'routing_key': 'workflow.load',
    },
    'workflow.tasks.on_workflow_error': {
        'queue': 'load',
        'routing_key': 'workflow.load',
    },
    'workflow.tasks.on_workflow_success': {
        'queue': 'load',
        'routing_key': 'workflow.load',
    },
}


imports = ('workflow.tasks', )
