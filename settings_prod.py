from settings_base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lisean_minerva',
        'USER': 'lisean_minerva',
        'PASSWORD': '1990106',
        'HOST': '',
        'PORT': '',
    }
}
