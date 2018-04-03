from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class User(models.Model):
    username = models.CharField(max_length=30, default="")
    password = models.CharField(max_length=300, default="")
    email = models.EmailField(default="")
    icon = models.ImageField(default="image/user_default/user.png")
    is_admin = models.BooleanField(default=True)
    #narodnost
    #sex ano

    def right_user(self, username, password):
        if username == self.username and self.password == password:
            return True
        return False

    def is_registred(self, username):
        if username == self.username:
            return True
        return False

    def __str__(self):
        return str(self.username)


class Event(models.Model):
    name = models.CharField(max_length=30, default="")
    text = models.TextField(max_length=3000, default="")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    users = models.TextField(null=True)

    def get_images(self):
        return Image.objects.filter(event=self)

    def get_comments(self):
        return Comment.objects.filter(event=self)

    def get_study_mat(self):
        return Study_material.objects.filter(event=self)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    image = models.CharField(max_length=300)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.TextField(max_length=300, default="")


class Anketa(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    points = models.IntegerField(default=1,
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(1)
                                 ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    question = models.CharField(default="", max_length=100)

class Study_material(models.Model):
    name = models.CharField(max_length=300)
    path = models.CharField(max_length=300)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)