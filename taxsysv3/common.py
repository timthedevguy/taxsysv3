import os
import sys
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://c973798b071c457c937ab6e646ff1cfc@sentry.io/1761193",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

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
    'huey.contrib.djhuey',
    'apps.testesi',
    'apps.testauth',
    'apps.landlord',
    'apps.tenant',
    'apps.eveonline',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

TIME_ZONE = 'GMT'

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
    'apps.testauth.utils.TestOIDC',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'testauth.TestUser'
# https://sso.pleaseignore.com/auth/realms/auth-ng/.well-known/openid-configuration
OIDC_OP_JWKS_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/userinfo'
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 300
OIDC_RP_SIGN_ALGO = 'RS256'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True

OIDC_RP_SCOPES = 'openid urn:sso:corp:* urn:sso:characters esi-industry.read_character_mining.v1'
OIDC_DIRECTOR_RP_SCOPES = 'openid urn:sso:corp:* urn:sso:characters esi-corporations.read_corporation_membership.v1 esi-wallet.read_corporation_wallets.v1 esi-industry.read_character_mining.v1'

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

FORCE_ALT_REFRESH_INTERVAL = 14

# ESI/TEST ESI Base URLs
TESTESI_BASE_URL = 'https://auth.pleaseignore.com/'
ESI_BASE_URL = 'https://esi.evetech.net/'
# ESI/TEST ESI Endpoints in use
TESTESI_GET_CHARACTERS = 'esi/_/characters/{subject}'
TESTESI_GET_CHARACTER_INFO = 'esi/v4/characters/{character_id}'
TESTESI_GET_CORPORATION_JOURNAL = 'esi/v4/corporations/{corporation_id}/wallets/{wallet_number}/journal/'
TESTESI_CLIENT_SCOPES = 'esi-wallet.read_corporation_wallets.v1 urn:sso:characters'
ESI_UNIVERSE_NAME_SEARCH = 'v2/universe/names/'
ESI_GET_CORPORATION_HISTORY = 'v1/characters/{character_id}/corporationhistory'
EVEONLINE_SDE_TABLES = [
    'invTypes',
    'invTypeMaterials',
    'dgmTypeAttributes'
]

MARKET_REGION = '10000002'
MARKET_SYSTEM = 60003760

EVAL_REFINE_SKILL = [
    {
        'ice_refine_rate': [
            18025
        ],
        'moon_refine_rate': [
            46152,
            46153,
            46154,
            46155,
            46156
        ],
        'ore_refine_rate': [
            12180,
            12181,
            12182,
            12183,
            12184,
            12185,
            12186,
            12187,
            12188,
            12189,
            12190,
            12191,
            12192,
            12193,
            12194,
            12195
        ]
    }
]
