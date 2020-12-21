from django.http import JsonResponse, Http404
from .models import Character


def ajax_get_director_char_count(request, tenant_id):
    count = Character.objects.filter(user=request.user).count()
    return JsonResponse({'count': count}, safe=False)