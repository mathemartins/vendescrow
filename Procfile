web: daphne vendescrow.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery -A vendescrow worker -B --loglevel=info
