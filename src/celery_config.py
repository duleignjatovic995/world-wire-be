from celery import Celery

app = Celery()

app.autodiscover_tasks(["src.tasks"])
app.conf.worker_hijack_root_logger = False
