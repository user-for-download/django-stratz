import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("dj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'task-crontab': {
    #     'task': 'get_public_league',
    #     'schedule': crontab(minute=0, hour=8),
    # },
    # "task-crontab-teams": {
    #     "task": "dj.teams.tasks.check_and_save_pro_teams",
    #     "schedule": crontab(hour="6"),
    # },
    "task-crontab-leagues": {
        "task": "dj.leagues.tasks.check_and_save_leagues_data",
        "schedule": crontab(minute="*/55"),
    },
    # 'task-crontab-players': {
    #     'task': 'dj.players.tasks.check_and_save_pro_players',
    #     'schedule': crontab(hour='5'),
    # }
}
