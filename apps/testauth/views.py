import time
from django.views.generic import TemplateView
from django.contrib import auth
from django.http import Http404
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View
from ..tenant.models import Tenant
from apps.testesi import testesi_client

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

    def get(self, request, token=None):
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

        add_state_and_nonce_to_session(request, state, params, token)

        request.session['oidc_login_next'] = get_next_url(request, redirect_field_name)

        query = urlencode(params)
        redirect_url = '{url}?{query}'.format(url=self.OIDC_OP_AUTH_ENDPOINT, query=query)
        return HttpResponseRedirect(redirect_url)

    def get_extra_params(self, request):
        return self.get_settings('OIDC_AUTH_REQUEST_EXTRA_PARAMS', {})


class DirectorOIDCAuthenticationCallbackView(View):
    """OIDC client authentication callback HTTP endpoint"""

    http_method_names = ['get']

    @staticmethod
    def get_settings(attr, *args):
        return import_from_settings(attr, *args)

    @property
    def failure_url(self):
        return self.get_settings('LOGIN_REDIRECT_URL_FAILURE', '/')

    @property
    def success_url(self):
        # Pull the next url from the session or settings--we don't need to
        # sanitize here because it should already have been sanitized.
        next_url = self.request.session.get('oidc_login_next', None)
        return next_url or self.get_settings('LOGIN_REDIRECT_URL', '/')

    def login_failure(self):
        return HttpResponseRedirect(self.failure_url)

    def login_success(self, token=None):
        auth.login(self.request, self.user)

        # Figure out when this id_token will expire. This is ignored unless you're
        # using the RenewIDToken middleware.
        expiration_interval = self.get_settings('OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS', 60 * 15)
        self.request.session['oidc_id_token_expiration'] = time.time() + expiration_interval

        if token:
            # Get the tenant by the token
            try:
                tenant = Tenant.objects.get(token=token)
                return HttpResponseRedirect(f'/{tenant.identifier}/director/success/?token={tenant.token}')
            except ObjectDoesNotExist:
                # If the token is no longer valid
                raise Http404('Tenant not found')
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request):
        """Callback handler for OIDC authorization code flow"""

        if request.GET.get('error'):
            # Ouch! Something important failed.
            # Make sure the user doesn't get to continue to be logged in
            # otherwise the refresh middleware will force the user to
            # redirect to authorize again if the session refresh has
            # expired.
            if request.user.is_authenticated:
                auth.logout(request)
            assert not request.user.is_authenticated
        elif 'code' in request.GET and 'state' in request.GET:

            # Check instead of "oidc_state" check if the "oidc_states" session key exists!
            if 'oidc_states' not in request.session:
                return self.login_failure()

            # State and Nonce are stored in the session "oidc_states" dictionary.
            # State is the key, the value is a dictionary with the Nonce in the "nonce" field.
            state = request.GET.get('state')
            if state not in request.session['oidc_states']:
                msg = 'OIDC callback state not found in session `oidc_states`!'
                raise SuspiciousOperation(msg)

            # Get the nonce from the dictionary for further processing and delete the entry to
            # prevent replay attacks.
            nonce = request.session['oidc_states'][state]['nonce']

            token = None
            # Check if Tenant ID is part of session
            if 'token' in request.session['oidc_states'][state]:
                token = request.session['oidc_states'][state]['token']

            del request.session['oidc_states'][state]

            # Authenticating is slow, so save the updated oidc_states.
            request.session.save()
            # Reset the session. This forces the session to get reloaded from the database after
            # fetching the token from the OpenID connect provider.
            # Without this step we would overwrite items that are being added/removed from the
            # session in parallel browser tabs.
            request.session = request.session.__class__(request.session.session_key)

            kwargs = {
                'request': request,
                'nonce': nonce,
            }

            if token:
                kwargs['token'] = token

            self.user = auth.authenticate(**kwargs)

            if self.user and self.user.is_active:
                return self.login_success(token=token)
        return self.login_failure()


def add_state_and_nonce_to_session(request, state, params, token=None):
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
    # test = len(request.session['oidc_states'])
    if len(request.session['oidc_states']) >= limit:
        oldest_state = None
        oldest_added_on = time.time()
        for item_state, item in request.session['oidc_states'].items():
            if item['added_on'] < oldest_added_on:
                oldest_state = item_state
                oldest_added_on = item['added_on']
        if oldest_state:
            del request.session['oidc_states'][oldest_state]

    if token:
        request.session['oidc_states'][state] = {
            'nonce': nonce,
            'added_on': time.time(),
            'token': token
        }
    else:
        request.session['oidc_states'][state] = {
            'nonce': nonce,
            'added_on': time.time(),
        }


class DirectorLoginView(TemplateView):
    template_name = 'director_login.html'

    def get_context_data(self, **kwargs):
        access_token = testesi_client.get_access_token()
        context = super().get_context_data(**kwargs)
        try:
            context['tenant'] = Tenant.objects.get(token=context['token'])
        except ObjectDoesNotExist:
            raise PermissionDenied
        return context
