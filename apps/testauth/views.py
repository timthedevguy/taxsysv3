from django.shortcuts import render
import time

from django.contrib import auth
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.http import is_safe_url
from django.utils.module_loading import import_string
from django.views.generic import View

from mozilla_django_oidc.utils import (absolutify,
                                       import_from_settings)
from mozilla_django_oidc.views import get_next_url

try:
    from urllib.parse import urlencode
except ImportError:
    # Python < 3
    from urllib import urlencode


# Create your views here.
class DirectorOIDCAuthenticationRequestView(View):
    """OIDC client authentication HTTP endpoint"""

    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        super(DirectorOIDCAuthenticationRequestView, self).__init__(*args, **kwargs)

        self.OIDC_OP_AUTH_ENDPOINT = self.get_settings('OIDC_OP_AUTHORIZATION_ENDPOINT')
        self.OIDC_RP_CLIENT_ID = self.get_settings('OIDC_RP_CLIENT_ID')

    @staticmethod
    def get_settings(attr, *args):
        return import_from_settings(attr, *args)

    def get(self, request):
        """OIDC client authentication initialization HTTP endpoint"""
        state = get_random_string(self.get_settings('OIDC_STATE_SIZE', 32))
        redirect_field_name = self.get_settings('OIDC_REDIRECT_FIELD_NAME', 'next')
        reverse_url = self.get_settings('OIDC_AUTHENTICATION_CALLBACK_URL',
                                        'oidc_authentication_callback')

        params = {
            'response_type': 'code',
            'scope': self.get_settings('OIDC_DIRECTOR_RP_SCOPES', 'openid email'),
            'client_id': self.OIDC_RP_CLIENT_ID,
            'redirect_uri': absolutify(
                request,
                reverse(reverse_url)
            ),
            'state': state,
        }

        params.update(self.get_extra_params(request))

        if self.get_settings('OIDC_USE_NONCE', True):
            nonce = get_random_string(self.get_settings('OIDC_NONCE_SIZE', 32))
            params.update({
                'nonce': nonce
            })

        add_state_and_nonce_to_session(request, state, params)

        request.session['oidc_login_next'] = get_next_url(request, redirect_field_name)

        query = urlencode(params)
        redirect_url = '{url}?{query}'.format(url=self.OIDC_OP_AUTH_ENDPOINT, query=query)
        return HttpResponseRedirect(redirect_url)

    def get_extra_params(self, request):
        return self.get_settings('OIDC_AUTH_REQUEST_EXTRA_PARAMS', {})


def add_state_and_nonce_to_session(request, state, params):
    """
    Stores the `state` and `nonce` parameters in a session dictionary including the time when it
    was added. The dictionary can contain multiple state/nonce combinations to allow parallel
    logins with multiple browser sessions.
    To keep the session space to a reasonable size, the dictionary is kept at 50 state/nonce
    combinations maximum.
    """
    nonce = params.get('nonce')

    # Store Nonce with the State parameter in the session "oidc_states" dictionary.
    # The dictionary can store multiple State/Nonce combinations to allow parallel
    # authentication flows which would otherwise overwrite State/Nonce values!
    # The "oidc_states" dictionary uses the state as key and as value a dictionary with "nonce"
    # and "added_on". "added_on" contains the time when the state was added to the session.
    # With this value, the oldest element can be found and deleted from the session.
    if 'oidc_states' not in request.session or \
            not isinstance(request.session['oidc_states'], dict):
        request.session['oidc_states'] = {}

    # Make sure that the State/Nonce dictionary in the session does not get too big.
    # If the number of State/Nonce combinations reaches a certain threshold, remove the oldest
    # state by finding out
    # which element has the oldest "add_on" time.
    limit = import_from_settings('OIDC_MAX_STATES', 50)
    test = len(request.session['oidc_states'])
    if len(request.session['oidc_states']) >= limit:
        oldest_state = None
        oldest_added_on = time.time()
        for item_state, item in request.session['oidc_states'].items():
            if item['added_on'] < oldest_added_on:
                oldest_state = item_state
                oldest_added_on = item['added_on']
        if oldest_state:
            del request.session['oidc_states'][oldest_state]

    request.session['oidc_states'][state] = {
        'nonce': nonce,
        'added_on': time.time(),
    }
