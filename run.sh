#!/usr/bin/env bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
      echo "wait database"
done 

alembic upgrade head
python3 fake_db.py

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7557 --timeout 200
