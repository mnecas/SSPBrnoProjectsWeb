from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Image, Event


# Create your views here.
def index(request):
    return render(request, "index.html", {"events": Event.objects.all()})


def login(request):
    return render(request, "login.html", {"error": "Bad username or password!"})


def create_event(request):
    if request.method == "GET":
        return render(request, "create_event.html")
    else:
        name = request.POST.get("title", "")
        text = request.POST.get("text", "")
        images = request.POST.getlist('images')
        if name and text:
            event = Event(name=name, text=text)
            event.save()
            for img in images:
                img=img.replace(" ","_")
                Image(image=img, event=event).save()
        return redirect("/")


def add_event(request):
    return redirect("/")


def edit_event(request):
    return render(request, "")
