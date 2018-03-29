from django.contrib import admin
from .models import User, Event, Image, Comment, Anketa

# Register your models here.

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Anketa)
