import os
from .common import *


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'NAME'    : os.environ.get("DB_NAME"),
        'USER'    : os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'HOST'    : os.environ.get("DB_HOST"),
        'PORT'    : os.environ.get("DB_PORT")
    }
}

OIDC_RP_CLIENT_ID = os.environ.get("CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SOCIAL_AUTH_SSODOTTE_SCOPE = [
    os.environ.get("CLIENT_SCOPE"),
]

# HUEY = {
#     'connection': {
#         'host': 'redis'
#     }
# }
