from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab
from django.core.mail import EmailMultiAlternatives, send_mail
from kombu import Exchange, Queue


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishworkcore.settings')

app = Celery('wishworkcore')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'suggest-project-every-morning': {
#         'task': 'wishworkcore.profiles.tasks.send_mass_suggested_projects_email',
#         'schedule': crontab(hour=9, minute=30),
#     },
#     'backup-database': {
#         'task': 'celery.tasks.backup_database',
#         'schedule': crontab(minute=0, hour=0),
#     },
# }
#
# app.conf.task_default_queue = 'default'
# app.conf.task_queue_max_priority = 10
# app.conf.task_queues = (
#     Queue('default',
#           routing_key='task.#'
#           ),
#     Queue('backup_tasks',
#           routing_key='backup.#',
#           queue_arguments={'x-max-priority': 1}
#           ),
#     Queue('single_email_tasks',
#           routing_key='mail.#',
#           queue_arguments={'x-max-priority': 3}
#           ),
#     Queue('mass_email_tasks',
#           routing_key='mass-mail.#',
#           queue_arguments={'x-max-priority': 2}
#           ),
# )
#
# task_default_exchange = 'tasks'
# task_default_exchange_type = 'topic'
# task_default_routing_key = 'task.default'
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(3, test.s('hello'))
#     sender.add_periodic_task(7, test.s('world'))


@app.task(bind=True, default_retry_delay=10)
def send_mail_async(self, subject, from_email, to_email, text_content, html_content):
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as exc:
        self.retry(exc=exc)


@app.task()
def backup_database():
    pass
    #os.system('pg_dump -h wishworkstage.ir -p 7799 wishworkcore > /home/moh3en_ir/backups/wish_work.back')

