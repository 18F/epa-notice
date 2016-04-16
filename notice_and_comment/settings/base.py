# -*- coding: utf-8 -*-
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

CACHES['regs_gov_cache'] = {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': BROKER_URL,
    'KEY_PREFIX': 'regs.gov',
    'TIMEOUT': 60*60*24,
    'OPTIONS': {
        'IGNORE_EXCEPTIONS': True,
    }
}

ATTACHMENT_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
ATTACHMENT_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
ATTACHMENT_BUCKET = os.environ.get('S3_BUCKET')
REGS_GOV_API_URL = os.environ.get('REGS_GOV_API_URL')
REGS_GOV_API_LOOKUP_URL = os.environ.get('REGS_GOV_API_LOOKUP_URL')
REGS_GOV_API_KEY = os.environ.get('REGS_GOV_API_KEY')

CFR_CHANGES = {
    "2016_02749": {
        "versions": {
            "478": {"left": "2010-13392", "right": "2012-13762"}
        },
        "amendments": [
            {"instruction": """
                1. The authority citation for 27 CFR part 478 is revised to
                read as follows:""",
             "cfr_part": "478",
             "authority":
                '5 U.S.C. 552(a); 18 U.S.C. 847, 921-931; 44 U.S.C. 3504(h).'},
            {"instruction": u"""
                2. Section 478.11 is amended by adding a definition for the
                term “Nonimmigrant visa” in alphabetical order to read as
                follows:""",
             "cfr_part": "478",
             "changes": {"478-11-p242755046": []}},
            {"instruction": """
                3. Section 478.32 is amended by revising the introductory text
                of paragraphs (a)(5)(ii) and (d)(5)(ii), and by revising
                paragraph (f), to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-32-a-5-ii": [], "478-32-d-5-ii": [],
                         "478-32-f": []}},
            {"instruction": """
                4. Section 478.44 is amended by revising paragraph
                (a)(1)(iii), and by revising the second sentence in paragraph
                (b), to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-44-a-1-iii": [], "478-44-b": []}},
            {"instruction": """
                5. Section 478.45 is amended by revising the second sentence
                to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-45": []}},
            {"instruction": """
                6. Section 478.99 is amended by revising the introductory text
                of paragraph (c)(5) to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-99-c-5": []}},
            {"instruction": """
                7. Section 478.120 is revised to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-120": []}},
            {"instruction": """
                8. Section 478.124 is amended by revising paragraph
                (c)(3)(iii) to read as follows:""",
             "cfr_part": "478",
             "changes": {"478-124-c-3-iii": []}}
        ]
    }
}

WKHTMLTOPDF_PATH = os.getenv(
    'WKHTMLTOPDF_PATH',
    # Path to local binary installed with `fetch_wkhtmltox`
    os.path.join(
        os.path.dirname(__file__), '..', '..',
        'wkhtmltox', 'bin', 'wkhtmltopdf',
    ),
)
