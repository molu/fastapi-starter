#!/bin/bash
set -e
 
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8888}
LOG_LEVEL=${LOG_LEVEL:-info}

if [[ -n ${C_FORCE_ROOT} ]]; then
    exec celery -A app.services.celery worker -l info -Q main-queue
else
    while !</dev/tcp/${POSTGRES_HOST}/${POSTGRES_PORT}; 
        do echo "Waiting for database..." && sleep 1; 
    done;
    echo -e "[+] Running migrations..."
    cd ${APP_HOME}/app/db && alembic upgrade head && cd ${APP_HOME}
    case $ENVIRONMENT in
        prod)
            exec gunicorn -k uvicorn.workers.UvicornWorker --bind ${HOST}:${PORT} app.main:app
        ;;
        dev)
            exec uvicorn --reload --host ${HOST} --port ${PORT} --log-level ${LOG_LEVEL} app.main:app
        ;;
        test)
            exec pytest ${APP_HOME}/app/tests
        ;;
    esac
fi
