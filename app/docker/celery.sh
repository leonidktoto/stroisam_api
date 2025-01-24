#!/bin/bash

if [ "$1" = "celery" ]; then
    celery -A app.tasks.celery:celery_app worker --loglevel=INFO --pool=solo    
elif [ "$1" = "flower" ]; then
    celery -A app.tasks.celery:celery_app flower
fi
