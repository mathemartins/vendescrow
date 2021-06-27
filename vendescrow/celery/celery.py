import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendescrow.settings')

app = Celery('vendescrow')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_coins_data_from_coingecko_30s': {
        'task': 'coins.tasks.get_coins_data_from_coingecko',
        'schedule': 10.0
    }
}

app.autodiscover_tasks()


# web: daphne vendescrow.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker --settings=vendescrow.settings -v2