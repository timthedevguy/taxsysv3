import json
import requests
import base64
import time
from django.conf import settings


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


def get_access_token(request=None):
    # TODO: Probably need some error checking here
    # Create the required OIDC Data
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.OIDC_RP_CLIENT_ID,
        'client_secret': settings.OIDC_RP_CLIENT_SECRET,
        'scope': settings.TESTESI_CLIENT_SCOPES
    }
    # Make the Call
    response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data)
    # Get the results
    results = json.loads(response.text)
    # Return the access token
    return results['access_token']
