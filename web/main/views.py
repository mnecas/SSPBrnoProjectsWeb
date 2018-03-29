from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import Image, Event, User, Comment, Anketa


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
    elif request.method == "POST":
        username = request.session["username"]
        name = request.POST.get("title", "")
        text = request.POST.get("text", "")
        images = request.FILES.getlist('images')
        if name and text:
            event = Event(name=name, text=text, creator=User.objects.filter(username=username).first())
            event.save()
            for img in images:
                fs = FileSystemStorage(location="media/image/events/" + name)
                fs.save(img.name, img)
                Image(image="image/events/"+name+"/"+img.name, event=event).save()

        return redirect("/")


def add_event(request):
    return redirect("/")


def edit_event(request):
    if request.method == "GET":
        event = request.GET.get("event", None)
        if event:
            user = None
            if "username" in request.session.keys():
                if request.session["username"]:
                    user = User.objects.filter(username=request.session["username"]).first()
            return render(request, "edit_event.html", {"event": Event.objects.filter(name=event).first(),
                                                       "user":user})
        else:
            return redirect("/")
    elif request.method == "POST":
        return redirect("/")


def info(request):
    if request.method == "GET":
        event_name = request.GET.get("event", None)
        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        if event_name:
            event = Event.objects.filter(name=event_name).first()
            ratings = Anketa.objects.filter(event=event)
            sum = 0
            for rtg in ratings:
                sum += rtg.points
            if len(ratings) > 0:
                avg = sum / len(ratings)
                resp = "%.2f" % avg
                return render(request, "info.html", {"event": event,
                                                     "user": user,
                                                     "average_rating": resp})
            return render(request, "info.html", {"event": event,
                                                 "user": user,
                                                 "average_rating": "none"})

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
            return redirect("/info?event=" + event.name)
        return redirect("/")


def edit_comment(request):
    pass


def remove_comment(request):
    if request.method == "GET":

        user = None
        if "username" in request.session.keys():
            if request.session["username"]:
                user = User.objects.filter(username=request.session["username"]).first()
        if not user.is_admin:
            return redirect("/")

        comment_id = request.GET.get("comment_id", "")
        event = request.GET.get("event", "")

        if comment_id:
            Comment.objects.filter(id=comment_id).first().delete()

        return redirect("/info?event=" + event)


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
            return redirect("/edit_event?event=" + event)
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

        return redirect("/info?event=" + event.name)
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
                fs = FileSystemStorage(location="media/image/events/" + name)
                fs.save(img.name, img)
        return redirect("/")
    elif request.method == "GET":
        return redirect("/")
