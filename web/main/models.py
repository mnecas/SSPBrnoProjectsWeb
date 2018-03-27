from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class User(models.Model):
    username = models.CharField(max_length=30, default="")
    password = models.CharField(max_length=300, default="")
    email = models.EmailField(default="")

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

    def get_images(self):
        return Image.objects.filter(event=self)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    image = models.ImageField(storage=fs)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
