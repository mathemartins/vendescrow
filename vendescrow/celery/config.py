from django.conf.global_settings import TIME_ZONE

uri = "redis://:p12286adb76f779078f6150f39f80ebf968e3aaf9ce86e9ed5567dcaf05f1f0bb@ec2-35-171-39-153.compute-1.amazonaws.com:23310"

# Celery Settings
CELERY_BROKER_URL = uri
CELERY_RESULT_BACKEND = uri
BROKER_POOL_LIMIT = None
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
