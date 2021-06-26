web: daphne vendescrow.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=vendescrow.settings -v2
celery -A vendescrow worker -l info
celery -A vendescrow beat -l info