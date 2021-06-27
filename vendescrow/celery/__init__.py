from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

# You can use rabbitmq instead here.
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'uri = "redis://:p12286adb76f779078f6150f39f80ebf968e3aaf9ce86e9ed5567dcaf05f1f0bb@ec2-35-171-39-153.compute-1.amazonaws.com:23310"')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendescrow.settings')

app = Celery('vendescrow')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

app.conf.beat_schedule = {
    'get_coins_data_from_coingecko_30s': {
        'task': 'coins.tasks.get_coins_data_from_coingecko',
        'schedule': 30.0
    }
}

# this allows you to schedule items in the Django admin.
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


# web: daphne vendescrow.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker --settings=vendescrow.settings -v2
