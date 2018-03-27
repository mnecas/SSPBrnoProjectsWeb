from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Image, Event, User


# Create your views here.
def index(request):
    return render(request, "index.html", {"events": Event.objects.all()})


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        password = request.POST.get("pass","")
        username = request.POST.get("username","")

        if User.objects.filter(username=username, password=password):
            request.session["username"] = username
            return redirect("/")
        return render(request, "login.html", {"error": "Bad username or password!"})


def create_event(request):
    if request.method == "GET":
        return render(request, "create_event.html")
    else:
        name = request.POST.get("title", "")
        text = request.POST.get("text", "")
        ##TOTO NEFUNGUJE
        for file in request.FILES.values():
            print(file)
        print( request.FILES)
        images=request.FILES.getlist('images')
        print(images)
        if name and text:
            event = Event(name=name, text=text)
            event.save()
            for img in images:
                fs = FileSystemStorage()
                fs.save(img.name, img)

                img = img.replace(" ", "_")
                Image(image=img, event=event).save()
        #YEP TOHLE

        return redirect("/")


def add_event(request):
    return redirect("/")


def edit_event(request):
    if request.method == "GET":
        event = request.GET.get("event", None)
        if event:
            return render(request, "edit_event.html", {"event": Event.objects.filter(name=event).first()})
        else:
            return redirect("/")
    else:
        return redirect("/")


def info(request):
    if request.method == "GET":
        event_name = request.GET.get("event", None)
        if event_name:
            event = Event.objects.filter(name=event_name).first()
            return render(request, "info.html", {"event": event})


def remove_image(request):
    if request.method == "GET":
        img = request.GET.get("img", None)
        event = request.GET.get("event", None)
        if img and event:
            Image.objects.filter(image=img).first().delete()
            return redirect("/edit_event?event=" + event)
        else:
            return redirect("/")


def save_edit(request):
    if request.method == "POST":
        name = request.POST.get("title", "")
        event_id = request.POST.get("event_id", "")
        text = request.POST.get("text", "")
        images = request.POST.getlist('images')
        event = Event.objects.filter(id=event_id)
        event.update(name=name, text=text)
        for img in images:
            img = img.replace(" ", "_")
            Image.objects.get_or_create(image=img, event=event.first())
        return redirect("/")
    else:
        return redirect("/")
