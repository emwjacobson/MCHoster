#!/bin/bash

set -e

wait-for-it.sh db:3306

python3 manage.py makemigrations
python3 manage.py migrate

if [[ $DEBUG == "True" ]]; then
    python3 manage.py runserver --insecure 0:8000
else
    gunicorn -w 4 -b 0.0.0.0:8000 mcweb.wsgi
fi