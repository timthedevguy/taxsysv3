from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import resolve_url


class TenantPermissionRequireMixin(PermissionRequiredMixin):
    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None or 'tenant_id' not in self.kwargs:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().  {0} should only use this Mixin if a child page of a tenant.'.format(
                    self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (f'tenant.tenant_{self.kwargs["tenant_id"]}_{self.permission_required}',)
        else:
            perms = f'tenant.tenant_{self.kwargs["tenant_id"]}_{self.permission_required}'
        return perms
