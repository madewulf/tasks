from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Task, List
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def index(request):
    return JsonResponse({'result': 'Welcome to the teamli.st API'})


@csrf_exempt
def l(request, key=None):
    if key is None:
        if request.method == 'POST':
            body = json.loads(request.body)
            name = body.get("name", None)
            description = body.get("description", None)
            li = List(name=name, description=description)
            li.save()
            return JsonResponse(li.as_dict())
        else:
            return JsonResponse({"lists": list(map(lambda li: li.as_dict(), List.objects.all()))})
    else:
        if request.method == 'PUT':
            li = get_object_or_404(List, key=key)
            body = json.loads(request.body)
            name = body.get("name", None)
            description = body.get("description", None)
            li.name = name
            li.description = description
            li.save()
            return JsonResponse(li.as_dict())
        elif request.method == 'DELETE':
            li = get_object_or_404(List, key=key)
            li.delete()
            return JsonResponse({"result": "deleted"})
        else :
            the_list = get_object_or_404(List, key=key)
    return JsonResponse(the_list.as_dict())


@csrf_exempt
def task(request, key=None):
    if key is None:
        if request.method == 'POST':
            body = json.loads(request.body)
            list_key = body.get('list', None)
            li = get_object_or_404(List, key=list_key)
            status = body.get("status", "waiting")
            text = body.get("text", None)
            index = body.get("index", 0)

            task = Task(list=li, status=status, text=text, index=index)
            task.save()
            return JsonResponse(task.as_dict())
        else:
            return JsonResponse({"error": "You should specify a task key"}, status_code=404)
    else:
        if request.method == 'GET':
            t = get_object_or_404(Task, key=key)
            return JsonResponse(t.as_dict())
        elif request.method == 'PUT':
                task = get_object_or_404(Task, key=key)
                body = json.loads(request.body)
                list_key = body.get('list', None)
                lists = List.objects.filter(key=list_key)
                li = None
                if lists:
                    li = lists[0]
                status = body.get("status", None)
                text = body.get("text", None)
                index = body.get("index", None)

                if li:
                    task.list = li
                if status:
                    task.status = status
                if text:
                    task.text = text
                if index:
                    task.index = index
                task.status
                task.save()
                return JsonResponse(task.as_dict())
        elif request.method == 'DELETE':
            task = get_object_or_404(Task, key=key)
            task.delete()
            return JsonResponse({"result": "deleted"})
        else:
            return JsonResponse({"error": "Cannot post on existing task"}, status_code=400)

    return JsonResponse({"message": "No task key specified"})

