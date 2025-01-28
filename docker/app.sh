#!/bin/bash
alembic upgrade head    

if [ "$1" = "gunicorn" ]; then
    gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
elif [ "$1" = "pytest" ]; then
    pytest -c ci_pytest.ini -vv
fi