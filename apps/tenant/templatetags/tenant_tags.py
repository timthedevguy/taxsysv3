from django import template
from apps.testauth.models import TestUser

register = template.Library()


@register.simple_tag()
def get_tenant_perm(user: TestUser, tenant_id):
    if user.has_perm(f'tenant.tenant_{tenant_id}_ceo'):
        return 4
    elif user.has_perm(f'tenant.tenant_{tenant_id}_admin'):
        return 3
    elif user.has_perm(f'tenant.tenant_{tenant_id}_accountant'):
        return 2
    elif user.has_perm(f'tenant.tenant_{tenant_id}_auditor'):
        return 1

    return 0


@register.simple_tag(takes_context=True)
def get_wizard_enabled(context):
    request = context['request']
    if 'wizard' in request.session:
        return True

    return False
