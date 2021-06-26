web: gunicorn vendescrow.asgi --log-file -

celery -A vendescrow worker -l info

celery -A vendescrow beat -l info