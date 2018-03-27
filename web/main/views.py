from django.shortcuts import render

from django.http import HttpResponse
from .models import Image
# Create your views here.
def index(request):
    return render(request, "index.html", {"images": Image.objects.all()})

def login(request):
    return render(request, "login.html", {"error": "Bad username or password!"})
