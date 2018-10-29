from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    url_key = models.CharField(max_length=10)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    modified_at = models.DateTimeField('date modified', auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    status = models.CharField(max_length=10, default='waiting')
    text = models.TextField()
    index = models.IntegerField(default=0)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    modified_at = models.DateTimeField('date modified', auto_now=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lists = models.ManyToManyField(List)
    tasks = models.ManyToManyField(Task)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    modified_at = models.DateTimeField('date modified', auto_now=True)
