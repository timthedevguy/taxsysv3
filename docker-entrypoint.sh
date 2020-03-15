#!/bin/sh

python /code/manage.py migrate
python /code/manage.py collectstatic --no-input

exec "$@"
