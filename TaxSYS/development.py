# Python imports
from os.path import join

# project imports
from .common import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

SOCIAL_AUTH_SSODOTTE_KEY = 'dev-taxsys-v3-binary'
SOCIAL_AUTH_SSODOTTE_SECRET = 'a84ed5f5-ad6d-4a74-8152-fbdb70ce48be'
SOCIAL_AUTH_SSODOTTE_SCOPE = [
    'openid urn:sso:corp:* urn:sso:characters esi-industry.read_character_mining.v1',
]

# adjust the minimal login
# LOGIN_URL = 'core_login'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = 'core_login'


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'taxsysv3',
        'USER'    : 'root',
        'PASSWORD': '44891620a',
        'HOST'    : '10.0.1.14',
        'PORT'    : '3306'
    }
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS
