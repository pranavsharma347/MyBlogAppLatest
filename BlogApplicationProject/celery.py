import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','BlogApplicationProject.settings')
app=Celery('BlogApplicationProject')
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings')

app.conf.beat_schedule={
    "share":{
        'task':'BlogApp.task.signup_mail',#note this task specify in task.py
        'schedule':10.0,
        'args':('new','new','pranavsharma886@gmail.com')
    }
}
app.conf.beat_scheduler='django_celery_beat.schedulers.DatabaseScheduler'

app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'request:{self.request!r}')
