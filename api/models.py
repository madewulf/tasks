from django.db import models
from django.db.models.functions import Lower
import random


def random_key():
    charset = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(charset) for _ in range(5))


class List(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=36, default=random_key)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    modified_at = models.DateTimeField("date modified", auto_now=True)
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "url_key": self.key,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            #'creator': self.creator.as_dict(),
            "members": list(map(lambda profile: profile.as_dict(), self.profile_set.order_by("name"))),
            "tasks": list(map(lambda task: task.as_dict(), self.task_set.order_by("created_at"))),
        }

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class Task(models.Model):
    status = models.CharField(max_length=10, default="waiting")
    text = models.TextField()
    key = models.CharField(max_length=36, default=random_key)
    index = models.IntegerField(default=0)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    modified_at = models.DateTimeField("date modified", auto_now=True)

    def as_dict(self):
        return {
            "list": self.list.key,
            "status": self.status,
            "text": self.text,
            "key": self.key,
            "index": self.index,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "assigned_to": list(map(lambda task: task.as_dict(), self.profile_set.order_by(Lower("name")))),
        }

    def __str__(self):
        return "%s - %s - %s" % (self.list, self.index, self.text)


class Profile(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    lists = models.ManyToManyField(List)
    tasks = models.ManyToManyField(Task)
    key = models.CharField(max_length=36, default=random_key)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    modified_at = models.DateTimeField("date modified", auto_now=True)

    def as_dict(self):
        return {"name": self.name, "key": self.key}

    def __str__(self):
        return "%s - %s" % (self.name, self.key)
