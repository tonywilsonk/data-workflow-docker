#!/bin/bash

set -e;

if [ -n "${MONGO_INITDB_USERNAME:-}" ] && [ -n "${MONGO_INITDN_PASSWORD:-}" ]; then
	"${mongo[@]}" "$MONGO_INITDB_DATABASE" <<-EOJS

		db.createUser({
			user: $(_js_escape "$MONGO_USER_NAME"),
			pwd: $(_js_escape "$MONGO_USER_PASSWORD"),
			roles: [ { role: "readWrite", db: $(_js_escape "$MONGO_INITDB_DATABASE") } ]
			})
	EOJS
fi