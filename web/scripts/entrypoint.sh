#!/bin/sh

set -e

python3 manage.py collectstatic

wait-for-it.sh db:3306

python3 manage.py makemigrations
python3 manage.py migrate

gunicorn -w 4 -b 0.0.0.0:8000 mcweb.wsgi