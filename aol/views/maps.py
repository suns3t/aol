from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from aol.models import Lake

def home(request):
    """Displays the interactive map"""
    lakes = Lake.objects.all()
    return render(request, "home/map.html", {
        "lakes": lakes,
    })
