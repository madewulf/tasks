from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('l/<slug:url_key>/', views.l, name='list_api'),
]