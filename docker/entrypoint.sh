#!/bin/bash

wait_for() {
  host=$(printf "%s\n" "$1"| cut -d : -f 1)
  port=$(printf "%s\n" "$1"| cut -d : -f 2)
  shift 1
  
  while ! nc -z "$host" "$port"; do
    echo "Waiting for $host:$port..."
    sleep 2
  done
}

wait_for redis:6379
wait_for elasticsearch:9200

python manage.py migrate

exec "$@"
