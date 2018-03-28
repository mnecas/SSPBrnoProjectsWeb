from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Image, Event, User, Comment


# Create your views here.
def index(request):
    user = None
    if "username" in request.session.keys():
        if request.session["username"]:
            user = User.objects.filter(username=request.session["username"]).first()
    return render(request, "index.html",
                  {"events": Event.objects.all(),
                   "user": user})


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        password = request.POST.get("pass", "")
        username = request.POST.get("username", "")
        if User.objects.filter(username=username, password=password):
            request.session["username"] = username
            return redirect("/")
        return render(request, "login.html", {"error": "Bad username or password!"})


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        password = request.POST.get("pass1", "")
        password2 = request.POST.get("pass2", "")
        username = request.POST.get("username", "")
        if username and password and password2 and password == password2:
            if not User.objects.filter(username=username):
                user = User(username=username, password=password)
                user.save()
                request.session["username"] = username
                return redirect("/")
        return render(request, "register.html", {"error": "This user was registred or the passwords are not same!"})


def create_event(request):
    if request.method == "GET":
        return render(request, "create_event.html")
    else:
        name = request.POST.get("title", "")
        text = request.POST.get("text", "")
        images = request.FILES.getlist('images')
        if name and text:
            event = Event(name=name, text=text)
            event.save()
            for img in images:
                fs = FileSystemStorage()
                fs.save(img.name, img)
                Image(image=img, event=event).save()

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
        return redirect("/")
    else:
        if "username" in request.session.keys():
            user = request.session["username"]
            comment_text = request.POST.get("comment_text","")
            event_id = request.POST.get("event_id","")
            Comment(event=Event.objects.filter(id=event_id).first(),
                    user=User.objects.filter(username=user).first(),
                    text=comment_text).save()
        return redirect("/")

def edit_comment(request):
    pass

def remove_comment(request):
    if request.method == "GET":
        comment_id = request.GET.get("comment_id", "")
        if comment_id:
            Comment.objects.filter(id=comment_id).first().delete()
        return redirect("/")
def remove_image(request):
    if request.method == "GET":
        img = request.GET.get("img", None)
        event = request.GET.get("event", None)
        if img and event:
            Image.objects.filter(image=img).first().delete()
            return redirect("/edit_event?event=" + event)
        else:
            return redirect("/")


def user_settings(request):
    if request.method == "GET":
        user = User.objects.filter(username=request.session["username"]).first()
        return render(request, "user_settings.html",
                      {"events": Event.objects.all(),
                       "user": user})
    else:
        image = request.FILES['image']
        user = User.objects.filter(username=request.session["username"])
        fs = FileSystemStorage()
        fs.save(image.name, image)
        user.update(icon=image)
        return redirect("/user_settings")


def user_logout(request):
    del request.session["username"]
    return redirect("/")


def remove_event(request):
    if request.method == "GET":
        event = request.GET.get("event", None)
        if event:
            Event.objects.filter(name=event).first().delete()
        return redirect("/")


def save_edit(request):
    if request.method == "POST":
        name = request.POST.get("title", "")
        event_id = request.POST.get("event_id", "")
        text = request.POST.get("text", "")
        images = request.FILES.getlist('images')
        event = Event.objects.filter(id=event_id)
        event.update(name=name, text=text)
        for img in images:
            image, created = Image.objects.get_or_create(image=img, event=event.first())
            if created:
                fs = FileSystemStorage()
                fs.save(img.name, img)
        return redirect("/")
    else:
        return redirect("/")


def change_password(request):
    if request.method == "GET":
        return render(request, "change_pass.html")
    elif request.method == "POST":
        password = request.POST.get("pass1", "")
        password2 = request.POST.get("pass2", "")
        old_pass = request.POST.get("old_pass", "")
        username = request.session["username"]
        if old_pass and password and password2 and password == password2 and username:
            user = User.objects.filter(username=username)
            if user:
                user.update(password=password)
                user.save()
                return redirect("/edit_user.html")
        return render(request, "change_pass.html", {"error": "passwords are not same or old password is incorrect!"})
