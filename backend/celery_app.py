import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate-expense-reports-daily": {
        "task": "reports.tasks.periodic.generate_expense_reports_task",
        "schedule": crontab(hour=0, minute=0),
    },
}
