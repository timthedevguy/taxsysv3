from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import TestUser
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.urls import reverse
from mozilla_django_oidc.utils import absolutify


class TestOIDC(OIDCAuthenticationBackend):
    def create_user(self, claims):
        return TestUser.objects.create_user(claims['sub'],
                                            auth_id=claims['auth_id'],
                                            subject=claims['sub'],
                                            display_name=claims['character'],
                                            is_sync=claims['synchronized'])

    def get_or_create_user(self, access_token, id_token, payload):
        user = super().get_or_create_user(access_token, id_token, payload)
        user.refresh_token = payload['refresh_token']
        user.save();
        return user

    def update_user(self, user, claims):
        user.is_sync = claims['synchronized']
        user.save()
        return user

    def verify_claims(self, claims):
        return 'sub' in claims

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""

        self.request = request
        if not self.request:
            return None

        state = self.request.GET.get('state')
        code = self.request.GET.get('code')
        nonce = kwargs.pop('nonce', None)

        if not code or not state:
            return None

        reverse_url = self.get_settings('OIDC_AUTHENTICATION_CALLBACK_URL',
                                        'oidc_authentication_callback')

        token_payload = {
            'client_id': self.OIDC_RP_CLIENT_ID,
            'client_secret': self.OIDC_RP_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': absolutify(
                self.request,
                reverse(reverse_url)
            ),
        }

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get('id_token')
        access_token = token_info.get('access_token')

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        # Store the Refresh Token
        payload['refresh_token'] = token_info.get('refresh_token')

        if payload:
            self.store_tokens(access_token, id_token)
            try:
                return self.get_or_create_user(access_token, id_token, payload)
            except SuspiciousOperation as exc:
                return None

        return None

    def filter_users_by_claims(self, claims):
        subject = claims['sub']
        if not subject:
            return TestUser.objects.none()

        try:
            return TestUser.objects.filter(subject__iexact=subject)
        except:
            return TestUser.objects.none()
