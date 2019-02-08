from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Task, List, Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import json


@csrf_exempt
def index(request):
    return JsonResponse({"result": "This is the taskli.st API"})

@csrf_exempt
def account(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get('username', None)
        name = body.get('name', None)
        password = body.get('password', None)
        email = body.get('email', None)

        if not username or username == "":
            return JsonResponse({"error": "Username should not be blank", "error_code": "USERNAME_BLANK"}, status=400)

        same_email = User.objects.filter(email=email)
        if len(same_email) > 0 :
            return JsonResponse({"error": "email already used", "error_code": "EMAIL_ALREADY_USED"}, status=400)

        same_username = User.objects.filter(username=username)

        if len(same_username) > 0 :
            return JsonResponse({"error": "Username already used", "error_code": "USERNAME_ALREADY_USED"}, status=400)

        if not password or len(password) < 6:
            return JsonResponse({"error": "Password should be at least 6 letters", "error_code": "PASSWORD_TOO_SHORT"}, status=400)

        if not name or name == "":
            return JsonResponse({"error": "Name should not be blank", "error_code": "NAME_BLANK"}, status=400)

        if not email:
            return JsonResponse({"error": "Email should not be blank", "error_code": "EMAIL_BLANK"}, status=400)

        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({"error": "Invalid email address", "error_code": "INVALID_EMAIL"}, status=400)

        u = User()
        u.username = username
        u.email = email
        u.save()
        u.set_password(password)
        p = Profile()
        p.user = u
        p.name = name
        p.save()
        return JsonResponse({"token": p.auth_token, "profile": p.as_dict()})

@csrf_exempt
def login(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get('username', None)
        password = body.get('password', None)
        u = authenticate(username=username, password=password)
        if u:
            profile = get_object_or_404(Profile, user=u)
            return JsonResponse({"token": profile.auth_token, "profile": profile.as_dict()})
        else:
            return JsonResponse({"token": None}, status=401)


@csrf_exempt
def l(request, key=None):
    if key is None:
        if request.method == "POST":
            body = json.loads(request.body)
            name = body.get("name", None)
            description = body.get("description", None)
            li = List(name=name, description=description)
            li.save()
            return JsonResponse(li.as_dict())
        else:
            token = request.META.get("HTTP_X_TASKLIST_TOKEN", None)
            profile = Profile.objects.filter(auth_token=token).first()
            if profile:
                return JsonResponse({"lists": [li.as_dict(False) for li in profile.lists.order_by('id')]})
            else:

                return JsonResponse({"lists": None})
    else:
        if request.method == "PUT":
            li = get_object_or_404(List, key=key)
            body = json.loads(request.body)
            name = body.get("name", None)
            users = body.get("users", None)

            if users:
                for key in users:
                    profile = Profile.objects.get(key=key)
                    li.profile_set.add(profile)
            description = body.get("description", None)
            if name:
                li.name = name
            if description:
                li.description = description
            sort = body.get("sort", None)
            if sort:
                li.sort = sort
            assignations_on = body.get("assignationsOn", None)
            if assignations_on is not None:
                li.assignations_on = assignations_on
            li.save()

            return JsonResponse(li.as_dict())
        elif request.method == "DELETE":
            li = get_object_or_404(List, key=key)
            li.delete()
            return JsonResponse({"result": "deleted"})
        else:
            the_list = get_object_or_404(List, key=key)
            token = request.META.get("HTTP_X_TASKLIST_TOKEN", None)
            if token:
                profile = Profile.objects.filter(auth_token=token).first()
                if profile:
                    profile.lists.add(the_list)
    return JsonResponse(the_list.as_dict())


@csrf_exempt
def task(request, key=None):
    if key is None:
        if request.method == "POST":
            body = json.loads(request.body)
            list_key = body.get("list", None)
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
        if request.method == "GET":
            t = get_object_or_404(Task, key=key)
            return JsonResponse(t.as_dict())
        elif request.method == "PUT":
            task = get_object_or_404(Task, key=key)
            body = json.loads(request.body)
            list_key = body.get("list", None)
            lists = List.objects.filter(key=list_key)
            li = None
            if lists:
                li = lists[0]
            status = body.get("status", None)
            text = body.get("text", None)
            index = body.get("index", None)
            users = body.get("users", None)
            if users:
                for key in users:
                    if key.startswith('-'):
                        key = key[1:]
                        profile = Profile.objects.get(key=key)
                        task.profile_set.remove(profile)
                    else:
                        profile = Profile.objects.get(key=key)

                        task.profile_set.add(profile)
            if li:
                task.list = li
            if status:
                task.status = status
            if text:
                task.text = text
            if index:
                task.index = index
            task.status
            if text is not None and text.strip() == "":
                task.delete()
                JsonResponse({"deleted": "ok"})
            else:
                task.save()
                return JsonResponse(task.as_dict())
        elif request.method == "DELETE":
            task = get_object_or_404(Task, key=key)
            task.delete()
            return JsonResponse({"result": "deleted"})
        else:
            return JsonResponse({"error": "Cannot post on existing task"}, status=400)

    return JsonResponse({"message": "No task key specified"})


@csrf_exempt
def user(request, key=None):
    if key is None:
        if request.method == "POST":
            body = json.loads(request.body)
            name = body.get("name", "None")
            profile = Profile(name=name)
            profile.save()
            return JsonResponse(profile.as_dict())
        else:
            return JsonResponse({"error": "You should specify a task key"}, status=404)
    else:
        if request.method == "GET":
            p = get_object_or_404(Profile, key=key)
            return JsonResponse(p.as_dict())
        elif request.method == "PUT":
            profile = get_object_or_404(Profile, key=key)
            body = json.loads(request.body)
            name = body.get("name", None)

            if name:
                profile.name = name
            profile.save()
            return JsonResponse(profile.as_dict())
        elif request.method == "DELETE":
            profile = get_object_or_404(Profile, key=key)
            profile.delete()
            return JsonResponse({"result": "deleted"})
        else:
            return JsonResponse({"error": "Cannot post on existing profile"}, status=400)

    return JsonResponse({"message": "No task key specified"})
