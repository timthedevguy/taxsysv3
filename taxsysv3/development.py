import os
from .common import *


SECRET_KEY = '8al3l685_12%qsf!0w5^vf1@=&wq&1*unlt++*+!k=obusve5('

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
