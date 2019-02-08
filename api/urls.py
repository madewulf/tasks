from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("l/", views.l, name="list_api"),
    path("l/<slug:key>/", views.l, name="list_api"),
    path("t/", views.task, name="task_api"),
    path("t/<slug:key>/", views.task, name="task_api"),
    path("u/", views.user, name="user_api"),
    path("login/", views.login, name="user_login"),
    path("account/", views.account, name="account_creation"),
    path("u/<slug:key>/", views.user, name="user_api"),
]
