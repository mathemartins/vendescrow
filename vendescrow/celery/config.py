from django.conf.global_settings import TIME_ZONE

uri = 'redis://:p2196718fddb40d4cae789847f5ce368fb6245550cb84eef2a45d41dd30ea202a@ec2-54-209-47-44.compute-1.amazonaws.com:23860'

# Celery Settings
CELERY_BROKER_URL = uri
CELERY_RESULT_BACKEND = "django-db"
BROKER_POOL_LIMIT = None
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# region Celery Settings
# CELERY_ACCEPT_CONTENT = ['json']
# # CELERY_RESULT_BACKEND = 'redis://:C@pV@lue2016@cvc.ma:6379/0'
# BROKER_URL = 'amqp://soufiaane:C@pV@lue2016@cvc.ma:5672/cvcHost'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_ACKS_LATE = True
# CELERYD_PREFETCH_MULTIPLIER = 1
#
# CELERY_REDIS_HOST = 'cvc.ma'
# CELERY_REDIS_PORT = 6379
# CELERY_REDIS_DB = 0
# CELERY_RESULT_BACKEND = 'redis'
# CELERY_RESULT_PASSWORD = "C@pV@lue2016"
# REDIS_CONNECT_RETRY = True
#
# AMQP_SERVER = "cvc.ma"
# AMQP_PORT = 5672
# AMQP_USER = "soufiaane"
# AMQP_PASSWORD = "C@pV@lue2016"
# AMQP_VHOST = "/cvcHost"
# CELERYD_HIJACK_ROOT_LOGGER = True
# CELERY_HIJACK_ROOT_LOGGER = True
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# endregion
