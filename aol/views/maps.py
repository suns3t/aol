from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from aol.models import Lake

def home(request):
    lakes = Lake.objects.all()
    return render(request, "home/map.html", {
        "lakes": lakes,
    })


