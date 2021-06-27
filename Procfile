web: gunicorn vendescrow.wsgi --log-file -
celery -A vendescrow worker -l INFO
celery -A vendescrow beat -l INFO