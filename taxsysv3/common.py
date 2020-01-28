import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(os.path.join(BASE_DIR, 'apps')))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.testauth_module',
    'apps.landlord_module',
    'apps.tenant_module'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'taxsysv3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'taxsysv3.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'node_modules'),
]

AUTHENTICATION_BACKENDS = [
    # 'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'apps.testauth_module.utils.TestOIDC',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'testauth_module.TestUser'
# https://sso.pleaseignore.com/auth/realms/auth-ng/.well-known/openid-configuration
OIDC_OP_JWKS_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/userinfo'
OIDC_RP_SIGN_ALGO = 'RS256'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
OIDC_STORE_ACCESS_TOKEN = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}
