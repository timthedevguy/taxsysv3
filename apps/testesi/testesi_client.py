import json
import requests
import base64
import time
from datetime import datetime, timedelta
from django.conf import settings


class AccessToken:
    __instance = None

    value = None
    expires = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AccessToken.__instance is None:
            AccessToken()
        return AccessToken.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AccessToken.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AccessToken.__instance = self

    def is_expired(self):
        if self.expires is not None:
            if datetime.now() < self.expires:
                return False

        return True




def get_characters(subject, **kwargs):
    return get(settings.TESTESI_GET_CHARACTERS, get_access_token(), subject=subject)


def get_character(character_id, **kwargs):
    return get(settings.TESTESI_GET_CHARACTER_INFO, get_access_token(), character_id=character_id)


def get_corporation_journal(corporation_id, wallet_number, **kwargs):
    return get(settings.TESTESI_GET_CORPORATION_JOURNAL, get_access_token(), corporation_id=corporation_id,
               wallet_number=wallet_number, **kwargs)

# test
def get(url, access_token, **kwargs):
    full_url = str.format('{}{}', settings.TESTESI_BASE_URL, str.format(url, **kwargs))
    headers = {'Authorization': str.format('JWT {}', access_token)}

    retries = 0

    while retries < 6:
        try:
            response = requests.get(full_url, headers=headers)
            break
        except:
            time.sleep(10)
            retries += 1
    else:
        raise Exception('No response')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception('NOT AUTHORIZED')

    return None


def get_access_token():
    token: AccessToken = AccessToken.get_instance()

    if token.is_expired():
        # Work on getting an Access Token
        data = {
            'grant_type': 'client_credentials',
            'client_id': settings.OIDC_RP_CLIENT_ID,
            'client_secret': settings.OIDC_RP_CLIENT_SECRET,
            'scope': settings.TESTESI_CLIENT_SCOPES
        }

        # Make the call
        response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data)
        # Get the results
        results = json.loads(response.text)

        token.value = results['access_token']
        token.expires = datetime.now() + timedelta(seconds=(results['expires_in'] - 15))

    return token.value
