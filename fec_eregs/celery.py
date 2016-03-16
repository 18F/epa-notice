from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fec_eregs.settings.dev')

from django.conf import settings

app = Celery('fec-eregs')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ('regulations', ))
