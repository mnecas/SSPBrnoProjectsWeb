from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import Image, Event, User, Comment, Anketa, Study_material
from django.db.models import Avg

import json

json_dec = json.JSONDecoder()
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
        all_users = list(User.objects.all())
        return render(request, "create_event.html" , {"all_users":all_users})
    elif request.method == "POST":
        username = request.session["username"]
        name = request.POST.get("title", "")
        text = request.POST.get("text", "")
        images = request.FILES.getlist('images')
        if name and text:
            users_opt = request.POST.getlist("users_opt")
            users_list = []
            for user_add in users_opt:
                users_list.append(user_add)
            users = json.dumps(users_list)
            event = Event(name=name, text=text, users=users, creator=User.objects.filter(username=username).first())
            event.save()
            for img in images:
                fs = FileSystemStorage(location="media/image/events/" + name)
                fs.save(img.name, img)
                Image(image="image/events/"+name+"/"+img.name, event=event).save()
            files = request.FILES.getlist('files')
            for file in files:
                fs = FileSystemStorage(location="media/image/events/" + event.name)
                fs.save(file.name, file)
                Study_material.objects.create(event=event, path="media/image/events/" + event.name, name=file.name)


        return redirect("/")


def add_event(request):
    return redirect("/")


def edit_event(request):
    if request.method == "GET":
        event_id = request.GET.get("event", None)
        if event_id:
            user = None
            if "username" in request.session.keys():
                if request.session["username"]:
                    user = User.objects.filter(username=request.session["username"]).first()
            event = Event.objects.filter(id=event_id).first()
            try:
                users_list = json_dec.decode(event.users)
            except:
                users_list = []
            all_users = list(User.objects.all())
            for added_user in users_list:
                for user_in_all_users in all_users:
                    if added_user == user_in_all_users.username:
                        all_users.remove(User.objects.filter(username=added_user).first())
            return render(request, "edit_event.html", {"event": event,
                                                       "user":user, "added_users":users_list,
                                                       "all_users":all_users})
        else:
            return redirect("/")
    elif request.method == "POST":
        return redirect("/")



def remove_event(request):
    if request.method == "GET":

        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        if not user.is_admin:
            return redirect("/")

        event = request.GET.get("event", None)
        if event:
            Event.objects.filter(id=event).first().delete()
        return redirect("/")


def info(request):
    if request.method == "GET":
        evet_id = request.GET.get("event", None)
        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        if evet_id:
            event = Event.objects.filter(id=evet_id).first()
            ratings = Anketa.objects.filter(event=event)
            if len(ratings)>0:
               return render(request, "info.html", {"event": event,
                                                 "user": user,
                                                 "average_rating": "%.2f"%ratings.aggregate(Avg('points'))["points__avg"],
                                                 "study_material": event.get_study_mat()})

            return render(request, "info.html", {"event": event,
                                                 "user": user,
                                                 "average_rating": "none",
                                                 "study_material": event.get_study_mat()})
        return redirect("/")
    elif request.method == "POST":
        if "username" in request.session.keys():
            user = request.session["username"]
            comment_text = request.POST.get("comment_text", "")
            event_id = request.POST.get("event_id", "")
            event = Event.objects.filter(id=event_id).first()
            Comment(event=event,
                    user=User.objects.filter(username=user).first(),
                    text=comment_text).save()
            return redirect("/info?event=" + str(event.id))
        return redirect("/")


def edit_comment(request):
    if request.method == "GET":
        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()

        comment_id = request.GET.get("comment_id", "")
        comm = Comment.objects.filter(id=comment_id).first()
        return render(request, "edit_comment.html", {"comment": comm, "user":user})

    if request.method == "POST":
        comment_id = request.POST.get("comment_id", "")
        text = request.POST.get("text", "")
        comm = Comment.objects.filter(id=comment_id)
        comm.update(text=text)
        return redirect("/info?event="+str(comm.first().event.id))


def remove_comment(request):
    if request.method == "GET":

        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()

        comment_id = request.GET.get("comment_id", "")
        event_id = request.GET.get("event", "")

        if comment_id:
            Comment.objects.filter(id=comment_id).first().delete()

        return redirect("/info?event=" + str(event_id))


def remove_image(request):
    if request.method == "GET":

        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        if not user.is_admin:
            return redirect("/")

        img = request.GET.get("img", None)
        event = request.GET.get("event", None)
        if img and event:
            Image.objects.filter(image=img).first().delete()
            return redirect("/edit_event?event=" + str(event.id))
        else:
            return redirect("/")


def user_settings(request):
    if request.method == "GET":
        user = User.objects.filter(username=request.session["username"]).first()
        return render(request, "user_settings.html",
                      {"events": Event.objects.all(),
                       "user": user})
    elif request.method == "POST":
        try:
            image = request.FILES['image']
            user = User.objects.filter(username=request.session["username"])
            fs = FileSystemStorage(location="media/image/users")
            fs.save(image.name, image)
            user.update(icon=image)
        except:
            # USER HAVNT CHANGE ICON
            pass
        password = request.POST.get("pass1", "")
        password2 = request.POST.get("pass2", "")
        old_pass = request.POST.get("old_pass", "")
        username = request.session["username"]
        user = User.objects.filter(username=username)
        if user.first().password == old_pass and password and password2 and password == password2 and username:
            user.update(password=password)
        return redirect("/user_settings")


def user_logout(request):
    del request.session["username"]
    return redirect("/")


def rate(request):
    if request.method == "GET":
        value = request.GET.get("value", "")
        user_id = request.GET.get("user_id", "")
        event_id = request.GET.get("event_id", "")
        user = User.objects.filter(id=user_id).first()
        event = Event.objects.filter(id=event_id).first()
        rating, created = Anketa.objects.get_or_create(user=user, event=event)
        if created:
            rating.points = int(value)
            rating.save()

        return redirect("/info?event=" + str(event.id))
    return redirect("/")


def save_edit(request):
    if request.method == "POST":
        name = request.POST.get("title", "")
        event_id = request.POST.get("event_id", "")
        text = request.POST.get("text", "")
        images = request.FILES.getlist('images')
        users_opt = request.POST.getlist("users_opt")
        event = Event.objects.filter(id=event_id)
        try:
            users_list = json_dec.decode(event.first().users)
        except:
            users_list = []
        for user_add in users_opt:
            is_added = True
            for user_added in users_list:
                if user_added == user_add:
                    is_added = False
            if is_added:
                users_list.append(user_add)
        users = json.dumps(users_list)
        event.update(name=name, text=text, users=users)
        for img in images:
            image, created = Image.objects.get_or_create(image="image/events/"+name+"/"+img.name, event=event.first())
            if created:
                fs = FileSystemStorage(location="media/image/events/" + name)
                fs.save(img.name, img)
        return redirect("/")
    elif request.method == "GET":
        return redirect("/")

def study_material_save(request):
    if request.method == "GET":
        event_id = request.GET.get("event_id", "")
        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        event = Event.objects.filter(id=event_id).first()
        return render(request, "study_material_edit.html", {"user": user, "event": event})

    elif request.method == "POST":
        event_id = request.POST.get("event_id", "")
        files = request.FILES.getlist('files')
        event = Event.objects.filter(id=event_id).first()
        for file in files:
            fs = FileSystemStorage(location="media/image/events/" + event.name)
            fs.save(file.name, file)
            Study_material.objects.create(event=event, path="media/image/events/" + event.name, name=file.name)
        return redirect("/info?event=" + str(event.id))

def study_mat(request):
    if request.method == "GET":
        event_id = request.GET.get("event_id", "")
        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        event = Event.objects.filter(id=event_id).first()
        return render(request, "study_material.html", {"user": user, "event": event, "study_material":event.get_study_mat()})
    elif request.method == "POST":
        redirect("/")


def add_user(request):
    if request.method == "GET":
        return redirect("/")

    elif request.method == "POST":
        event_id = request.POST.get("event_id", "")
        user_add = request.POST.get("user_add","")
        event = Event.objects.filter(id=event_id)

        try:
            users_list = json_dec.decode(event.first().users)
        except:
            users_list = []
        users_list.append(user_add)
        users = json.dumps(users_list)
        event.update(users=users)
        return redirect("/info?event=" + str(event.first().id))