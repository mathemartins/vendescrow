web: gunicorn vendescrow.wsgi --log-file -
celery: celery worker -A vendescrow -l INFO
celery: celery beat -A vendescrow -l INFO
