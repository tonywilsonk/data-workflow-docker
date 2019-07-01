#!/usr/bin/env bash

# starting flask (default)
if [ $1 = 'flask' ]; then
	# run flask with gunicorn
    gunicorn --bind 0.0.0.0:5000 apis.wsgi:app
fi

#override command
exec "$@"