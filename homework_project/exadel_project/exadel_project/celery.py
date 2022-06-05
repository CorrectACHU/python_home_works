from celery import Celery
import os

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exadel_project.settings')

app = Celery('exadel_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'print-count-of-users-every-minute': {
        'task': 'client.tasks.count_clients',
        'schedule': crontab(minute='*/1')
    }
}
