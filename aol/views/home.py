from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from aol.models import Lake

def home(request):
    lakes = Lake.objects.all()
    return render(request, "home/home.html", {
        "lakes": lakes,
    })
