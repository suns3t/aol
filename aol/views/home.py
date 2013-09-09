from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from aol.models import Lake

def home(request):
    """The homepage of the site"""
    lakes = Lake.objects.all()
    return render(request, "home/home.html", {
        "lakes": lakes,
    })

def about(request):
    """The about page"""
    # maybe use flatpages for this instead?
    return render(request, "home/about.html", {

    })

def credits(request):
    """The credits page"""
    # maybe use flatpages for this instead?
    return render(request, "home/credits.html", {

    })
