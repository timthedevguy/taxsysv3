from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import TestUser
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured


class TestOIDC(OIDCAuthenticationBackend):
    def create_user(self, claims):
        return TestUser.objects.create_user(claims['sub'],
                                            auth_id=claims['auth_id'],
                                            subject=claims['sub'],
                                            display_name=claims['character'],
                                            is_sync=claims['synchronized'])

    def update_user(self, user, claims):
        user.is_sync = claims['synchronized']
        user.save()
        return user

    def verify_claims(self, claims):
        return 'sub' in claims

    def filter_users_by_claims(self, claims):
        subject = claims['sub']
        if not subject:
            return TestUser.objects.none()

        try:
            return TestUser.objects.filter(subject__iexact=subject)
        except:
            return TestUser.objects.none()
