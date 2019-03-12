# Python imports
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

SOCIAL_AUTH_SSODOTTE_KEY = '85b1a02b-3599-4287-bb22-e80a4b62eacc'
SOCIAL_AUTH_SSODOTTE_SECRET = '46b56def-f2ff-4944-a79b-7204a9fd240b'

# adjust the minimal login
#LOGIN_URL = 'core_login'
#LOGIN_REDIRECT_URL = '/'
#LOGOUT_REDIRECT_URL = 'core_login'


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taxsysv3',
        'USER': 'db_user',
        'PASSWORD': 'TI6510**',
        'HOST': '10.0.1.14',
        'PORT': '3306'
    }
}


# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS