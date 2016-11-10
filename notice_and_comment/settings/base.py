# -*- coding: utf-8 -*-
import os


from regcore.settings.base import *  # noqa
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *  # noqa
REGSITE_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS = ('overextends',
                  'notice_and_comment',) + REGCORE_APPS + REGSITE_APPS

DISABLE_ROBOTS = os.environ.get('DISABLE_ROBOTS')
ROOT_URLCONF = 'notice_and_comment.urls'

DATABASES = REGCORE_DATABASES

_port = os.environ.get('PORT', '8000')
if HTTP_AUTH_USER and HTTP_AUTH_PASSWORD:
    API_BASE = 'http://{}:{}@localhost:{}/api/'.format(
        HTTP_AUTH_USER, HTTP_AUTH_PASSWORD, _port)
else:
    API_BASE = 'http://localhost:{}/api/'.format(_port)

STATICFILES_DIRS = ['compiled']

# Commenting
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACKS_LATE = True

CACHES['regs_gov_cache'] = {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    # safe because: not used in prod and helpful locally
    'LOCATION': '/tmp/regs_gov_cache',  # nosec
    'KEY_PREFIX': 'regs.gov',
    'TIMEOUT': 60 * 60 * 24,
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
    "0000_0000": {
        "versions": {},
        "amendments": []
    },
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
             "changes": [["478-11-p242755046", []]]},
            {"instruction": """
                3. Section 478.32 is amended by revising the introductory text
                of paragraphs (a)(5)(ii) and (d)(5)(ii), and by revising
                paragraph (f), to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-32-a-5-ii", []],
                         ["478-32-d-5-ii", []],
                         ["478-32-f", []]]},
            {"instruction": """
                4. Section 478.44 is amended by revising paragraph
                (a)(1)(iii), and by revising the second sentence in paragraph
                (b), to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-44-a-1-iii", []],
                         ["478-44-b", []]]},
            {"instruction": """
                5. Section 478.45 is amended by revising the second sentence
                to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-45", []]]},
            {"instruction": """
                6. Section 478.99 is amended by revising the introductory text
                of paragraph (c)(5) to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-99-c-5", []]]},
            {"instruction": """
                7. Section 478.120 is revised to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-120", []]]},
            {"instruction": """
                8. Section 478.124 is amended by revising paragraph
                (c)(3)(iii) to read as follows:""",
             "cfr_part": "478",
             "changes": [["478-124-c-3-iii", []]]}
        ]
    }
}
PREAMBLE_INTRO = {
    "0000_0000": {
        "meta": {
            "primary_agency": "Environmental Protection Agency",
            "title": "EPA's new proposal",
            "comments_close": "2016-05-29",
            "publication": "2016-02-29",    # to be removed
            "publication_date": "2016-02-29",
            "cfr_parts": [{"title": "40", "parts": ["300"]}],  # to be removed
            "cfr_refs": [{"title": "40", "parts": ["300"]}],
            "dockets": ["EPA-HQ-SFUND-2010-1086",
                        "FRL-9925-69-OLEM"],
            "rins": ["2050-AG67"],  # to be removed
            "regulatory_id_numbers": ["2050-AG67"],
        }
    },
    "2016_02749": {
        "meta": {
            "primary_agency": "Environmental Protection Agency",
            "title": ("Addition of a Subsurface Intrusion Component to the "
                      "Hazard Ranking System"),
            "comments_close": "2016-04-29",
            "publication": "2016-02-29",    # to be removed
            "publication_date": "2016-02-29",
            "cfr_parts": [{"title": "40", "parts": ["300"]}],  # to be removed
            "cfr_refs": [{"title": "40", "parts": ["300"]}],
            "dockets": ["EPA-HQ-SFUND-2010-1086",
                        "FRL-9925-69-OLEM"],
            "rins": ["2050-AG67"],  # to be removed
            "regulatory_id_numbers": ["2050-AG67"],
        }
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

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

if os.getenv('WHOLE_SITE_AUTH'):
    MIDDLEWARE_CLASSES += (
        'notice_and_comment.basic_auth.BasicAuthMiddleware',
    )
