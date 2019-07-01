#!/usr/bin/env bash

# starting celery worker (default)
if [ $1 = 'worker' ]; then
	# run celery worker
    exec celery --app=workflow.celery:app worker --queues $WORKER_QUEUES --pool $WORKER_POOL --concurrency $WORKER_CONCURRENCY --hostname $WORKER_NAME --without-mingle --without-gossip --loglevel info

fi

# starting flower celery tasks monitoring
if [ $1 = 'flower' ]; then
	# run celery worker
    exec flower --app=workflow.celery:app --port=5555

fi

#override command
exec "$@"


