import json
import os

from cfenv import AppEnv
env = AppEnv()

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
REGS_API_URL = env.get_credential('REGS_API_URL', os.environ.get('REGS_API_URL'))
REGS_API_KEY = env.get_credential('REGS_API_KEY', os.environ.get('REGS_API_KEY'))
print("URL: {}, Key: {}".format(REGS_API_URL, REGS_API_KEY))
