import os
from .common import *


SECRET_KEY = '8al3l685_12%qsf!0w5^vf1@=&wq&1*unlt++*+!k=obusve5('

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'NAME'    : 'taxsys',
        'USER'    : 'taxsys',
        'PASSWORD': 'TI6510**',
        'HOST'    : 'psql01.binarymethod.com',
        'PORT'    : ''
    }
}

OIDC_RP_CLIENT_ID = 'dev-taxsys-v3-binary'
OIDC_RP_CLIENT_SECRET = 'a84ed5f5-ad6d-4a74-8152-fbdb70ce48be'
SOCIAL_AUTH_SSODOTTE_SCOPE = [
    'openid urn:sso:corp:* urn:sso:characters esi-industry.read_character_mining.v1',
]

