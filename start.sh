#!/bin/sh

set -e

echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running start.sh"

env=${APP_ENV:-development}

if [ $env = "production" ]
then
    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running migrations"
    # alembic upgrade head

    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running production environment"
    gunicorn --bind 0.0.0.0:5000 --chdir ./ms_fa main:app -k uvicorn.workers.UvicornWorker --timeout 120 --workers=2 --access-logfile /var/log/gunicorn-access.log --error-logfile /var/log/gunicorn-error.log --log-level info
elif [ $env = 'celery' ]
then
    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: start cron"
    /usr/sbin/crond -b -l 8

    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running celery worker"
    celery --app ms_fa.tasks.worker.celery worker --loglevel=INFO
elif [ $env = 'testing' ]
then
    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running testing environment"
    coverage run -m pytest
    coverage report
else
    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running migrations"
    # alembic upgrade head

    echo $(date '+%F %T.%3N %Z') "[fastapi] INFO: running development environment"
    uvicorn main:app --host=0.0.0.0 --port=5000 --reload
fi

