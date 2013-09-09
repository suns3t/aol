from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from aol.models import Lake

def listing(request):
    """Display a list of all the lakes in the Atlas, with pagination"""
    lakes = Lake.objects.all()
    return render(request, "lakes/listing.html", {
        "lakes": lakes,
    })

def detail(request, reachcode):
    """Display the detail view for an individual lake"""
    lake = get_object_or_404(Lake, reachcode=reachcode)
    return render(request, "lakes/detail.html", {
        "lake": lake,
    })

