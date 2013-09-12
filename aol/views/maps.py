from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from aol.models import Lake, LakeGeom

def home(request):
    """Displays the interactive map"""
    lakes = Lake.objects.all()
    return render(request, "maps/map.html", {
        "lakes": lakes,
    })

def lakes(request):
    """Return the KML for the lakes"""
    scale = int(request.GET['scale'])
    bbox = request.GET['bbox_limited'].split(",")

    lakes = LakeGeom.objects.toKML(scale=scale)
    return render(request, "maps/lakes.kml", {
        "lakes": lakes,
    })


