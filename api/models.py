from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
import random


def random_key(length=8):
    charset = "abcdefghijklmnopqrstuvwxyz1234567890"
    return "".join(random.choice(charset) for _ in range(length))


class List(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=36, default=random_key)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    modified_at = models.DateTimeField("date modified", auto_now=True)
    sort = models.CharField(max_length=10, default="created_at")
    assignations_on = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def as_dict(self, complete=True):
        res = {
            "name": self.name,
            "description": self.description,
            "url_key": self.key,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "sort": self.sort,
            "assignationsOn": self.assignations_on,
            #'creator': self.creator.as_dict(),
        }

        if complete:
            res["members"] = list(
                map(
                    lambda profile: profile.as_dict(), self.profile_set.order_by("name")
                )
            )
            res["tasks"] = list(
                map(
                    lambda task: task.as_dict(),
                    self.task_set.order_by(*self.sort.split(",")),
                )
            )

        return res

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
            "assigned_to": list(
                map(
                    lambda task: task.as_dict(),
                    self.profile_set.order_by(Lower("name")),
                )
            ),
        }

    def __str__(self):
        return "%s - %s - %s" % (self.list, self.index, self.text)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auth_token = models.CharField(max_length=20, default=random_key)
    name = models.TextField()
    lists = models.ManyToManyField(List)
    lists_to_notify = models.ManyToManyField(List, related_name="users_to_notify")
    tasks = models.ManyToManyField(Task)
    key = models.CharField(max_length=36, default=random_key)
    private_key = models.CharField(max_length=36, default=random_key)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    modified_at = models.DateTimeField("date modified", auto_now=True)

    def as_dict(self):
        return {"name": self.name, "key": self.key}

    def __str__(self):
        return "%s - %s" % (self.name, self.key)


class Event(models.Model):
    TASK_DONE = "task_done"
    TASK_UNDONE = "task_undone"
    LIST_COMPLETED = "list_completed"
    TASK_ADDED = "task_added"
    LIST_CREATED = "list_created"
    TASK_EDITED = "task_edited"
    LIST_EDITED = "list_edited"

    TYPE_CHOICES = (
        (TASK_DONE, "Task done"),
        (TASK_UNDONE, "Task undone"),
        (LIST_COMPLETED, "List completed"),
        (TASK_ADDED, "Task added"),
        (LIST_CREATED, "List created"),
        (TASK_EDITED, "Task edited"),
        (LIST_EDITED, "List edited"),
    )
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    created_at = models.DateTimeField("date created", auto_now_add=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s - %s - %s - %s - %s - %s" % (
            self.list,
            self.task,
            self.profile,
            self.type,
            self.old_value,
            self.new_value,
        )
