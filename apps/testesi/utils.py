import json
import requests
import base64
import time
from django.conf import settings


class TestClient:
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
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

        return None

    def get_access_token(request=None):
        if request is None:
            # This is a client token
            data = {'grant_type': 'client_credentials', 'client_id': settings.OIDC_RP_CLIENT_ID,
                    'client_secret': settings.OIDC_RP_CLIENT_SECRET}
            response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data)
            results = json.loads(response.text)
        else:
            # This is a user token
            # Check if access token is expired or not
            token_expiration = request.session.get('oidc_id_token_expiration')
            if token_expiration > time.time():
                return request.session.get('oidc_access_token')

            data = {'grant_type': 'refresh_token', 'refresh_token': request.user.refresh_token}
            auth = str(base64.b64encode(str.format('{}:{}', settings.OIDC_RP_CLIENT_ID, settings.OIDC_RP_CLIENT_SECRET).encode('utf-8')), 'utf-8')
            headers = {'Authorization': str.format('Basic {0}', auth)}
            response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data, headers=headers)
            results = json.loads(response.text)

            # Sanity check
            if response.status_code is 200 and 'refresh_token' in results:
                # Update User with new Refresh Token
                request.user.refresh_token = results['refresh_token']
                request.user.save()
                # Update our session with Expire and Access Token, saves calls to endpoint
                request.session['oidc_id_token_expiration'] = time.time() + results['expires_in']
                request.session['oidc_access_token'] = results['access_token']
            else:
                # TODO: Raise Error for Sentry
                return None

        return results['access_token']
