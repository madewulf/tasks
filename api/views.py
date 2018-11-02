from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Task, List


def index(request):
    return JsonResponse({'result': 'Welcome to the teamli.st API'})


def l(request, url_key):
    the_list = get_object_or_404(List, key=url_key)
    return JsonResponse(the_list.as_dict())
