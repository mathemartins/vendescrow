web: gunicorn vendescrow.wsgi --log-file -
worker: celery -A vendescrow worker --beat -S django -l info
