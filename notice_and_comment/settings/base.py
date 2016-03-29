import os


from regcore.settings.base import *  # noqa
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *  # noqa
REGSITE_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS = ('overextends', 'notice_and_comment',) + REGCORE_APPS + REGSITE_APPS

ROOT_URLCONF = 'notice_and_comment.urls'

DATABASES = REGCORE_DATABASES

API_BASE = 'http://localhost:{}/api/'.format(
    os.environ.get('VCAP_APP_PORT', '8000'))

STATICFILES_DIRS = ['compiled']

# Commenting
BROKER_URL = 'redis://localhost:6379/0'

ATTACHMENT_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
ATTACHMENT_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
ATTACHMENT_BUCKET = os.environ.get('S3_BUCKET')
REGS_GOV_API_URL = os.environ.get('REGS_GOV_API_URL')
REGS_GOV_API_KEY = os.environ.get('REGS_GOV_API_KEY')
