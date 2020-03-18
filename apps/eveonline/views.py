from django.shortcuts import render
from django.http import JsonResponse
from .models import Type


# Create your views here.
def type_name_search(request):
    if 'term' in request.GET:
        test = request.GET['term']
        found_types = Type.objects.filter(typeName__istartswith=request.GET['term'])

        results = []
        found_type: Type
        for found_type in found_types:
            results.append({"id": found_type.typeID, "text": found_type.typeName})

        return JsonResponse({'results': results}, safe=False)

    return JsonResponse({'results': None}, safe=False)
