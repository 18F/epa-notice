from __future__ import absolute_import

from notice_and_comment import newrelic
newrelic.initialize()

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notice_and_comment.settings.dev')

from django.conf import settings

app = Celery('notice_and_comment')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ('regulations', ))
