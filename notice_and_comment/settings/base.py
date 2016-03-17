import json
import os

from regcore.settings.base import *
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *
REGSITE_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS = ('overextends', 'notice_and_comment',) + REGCORE_APPS + REGSITE_APPS

ROOT_URLCONF = 'notice_and_comment.urls'

DATABASES = REGCORE_DATABASES

API_BASE = 'http://localhost:{}/api/'.format(
    os.environ.get('VCAP_APP_PORT', '8000'))

STATICFILES_DIRS = ['compiled']

# Commenting
BROKER_URL = 'redis://localhost:6379/0'
REGS_API_BASE = 'https://api.data.gov/TEST/regulations/v3/comment'
REGS_API_URL = '{}?api_key={}'.format(
    REGS_API_BASE, os.environ.get('REGS_API_KEY', 'DEMO_KEY'))
