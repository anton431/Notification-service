import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification.settings")

app = Celery("notification")
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks()