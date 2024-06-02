from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local_settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.config_from_object("celeryconf.connection")
app.autodiscover_tasks()

app.conf.beat_schedule = {}
