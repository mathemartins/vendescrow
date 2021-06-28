web: gunicorn vendescrow.wsgi --log-file -
worker: celery -A vendescrow worker -B --loglevel=info
