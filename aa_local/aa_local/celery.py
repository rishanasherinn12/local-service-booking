import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aa_local.settings')

app = Celery('aa_local')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()