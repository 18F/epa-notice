from .base import *

DEBUG = True

# Analytics settings

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
BUCKET = os.environ.get('S3_BUCKET')

try:
    from local_settings import *
except ImportError:
    pass
