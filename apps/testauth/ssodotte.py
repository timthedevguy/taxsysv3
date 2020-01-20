from social_core.backends.oauth import BaseOAuth2, AuthFailed
from jwcrypto import jwk, jwt
from apps.landlord import settings
from apps.landlord.models import Setting
import requests
import json


class SSODotteOAuth2(BaseOAuth2):
    name = 'ssodotte'
    BASE_URL = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect'
    AUTHORIZATION_URL = BASE_URL + '/auth'
    ACCESS_TOKEN_URL = BASE_URL + '/token'
    ID_KEY = 'auth_id'
    USERNAME_KEY = 'sub'
    ACCESS_TOKEN_METHOD = 'POST'
    STATE_PARAMETER = False
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('CharacterID', 'id'),
        ('expires_in', 'expires'),
        ('CharacterOwnerHash', 'owner_hash', True),
        ('refresh_token', 'refresh_token', True),
    ]

    def get_user_details(self, response):
        """Return user details from EVE Online account"""
        user_data = self.user_data(response['access_token'])
        if is_token_valid(response['access_token']):
            if response['synchronized'] is True:
                # Get Sub here and provide in user details section
                return {
                    'username': response[self.USERNAME_KEY],
                    'email': '',
                    'fullname': response['character'],
                    'first_name': '',
                    'last_name': '',
                    'character_name': response['character'],
                    'character_id': response['character_id'],
                    'synchronized': response['synchronized'],
                    'subject': response['sub'],
                    'auth_id': response['auth_id']
                }
            else:
                raise AuthFailed(self)
        else:
            raise AuthFailed(self)

    def get_user_id(self, details, response):
        """Return unique ID for user, in this case auth_id"""
        return response.get(self.ID_KEY)


def validate_jwt(token):
    # Get Key from "https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs"
    raw_keys = requests.get('https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs')
    try:
        # Create JWK from raw data
        key = jwk.JWK(**raw_keys.json()['keys'][0])
        try:
            # Attempt to validate and decode
            decoded = jwt.JWT(key=key, jwt=token)
            return decoded
        except:
            # TODO: Report invalid cert to Sentry?
            pass
    except:
        # TODO: Report to Sentry?
        pass

    return None


def is_token_valid(token):
    # Get Key from "https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs"
    raw_keys = requests.get('https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect/certs')
    try:
        # Create JWK from raw data
        key = jwk.JWK(**raw_keys.json()['keys'][0])
        try:
            # Attempt to validate and decode
            decoded = jwt.JWT(key=key, jwt=token)
            return True
        except:
            # TODO: Report invalid cert to Sentry?
            return False
    except:
        # TODO: Report to Sentry?
        return False

    return False
