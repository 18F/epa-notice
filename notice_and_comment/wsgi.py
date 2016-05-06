from notice_and_comment import newrelic
newrelic.initialize()

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notice_and_comment.settings")
# important that the whitenoise import is after the line above
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
