#!/bin/bash
echo "Старт docker/app.sh ..."
alembic upgrade head    

if [ "$1" = "gunicorn" ]; then
    echo "Старт gunicorn..."
    gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
elif [ "$1" = "pytest" ]; then
    echo "Старт pytest..."
    pytest -c ci_pytest.ini -vv
fi