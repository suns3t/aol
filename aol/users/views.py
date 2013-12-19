from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from aol.lakes.models import Lake, Photo, Document, Photo, Plant 
from .forms import DocumentForm, LakeForm, PhotoForm, PlantForm

@login_required
def listing(request):
    """List all the lakes that the admin can edit"""
    lakes = Lake.objects.all()
    return render(request, "admin/listing.html", {
        "lakes": lakes,
    })

@login_required
def edit_lake(request, lake_id):
    """The edit page for a lake"""
    lake = get_object_or_404(Lake, lake_id=lake_id)
    if request.POST:
        form = LakeForm(request.POST, instance=lake)
        if form.is_valid():
            form.save()
            messages.success(request, "Lake Edited")
            return HttpResponseRedirect(reverse("admin-edit-lake", args=(lake.pk,)))
    else:
        form = LakeForm(instance=lake)

    photos = Photo.objects.filter(lake=lake)
    documents = Document.objects.filter(lake=lake)

    return render(request, "admin/edit_lake.html", {
        "lake": lake,
        "form": form,
        "photos": photos,
        "documents": documents,
    })

@login_required
def edit_photo(request, lake_id=None, photo_id=None):
    """
    The add/edit page for a photo. If a photo_id is passed in, we edit. If the
    lake_id is passed in, we create
    """
    try:
        photo = Photo.objects.get(pk=photo_id)
        lake = photo.lake
    except Photo.DoesNotExist:
        # create a new photo with a foreign key to the lake
        lake = get_object_or_404(Lake, pk=lake_id)
        photo = Photo(lake=lake)

    if request.POST:
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo %s" % "Edited" if photo_id else "Created")
            return HttpResponseRedirect(reverse("admin-edit-lake", args=(lake.pk,)))
    else:
        form = PhotoForm(instance=photo)

    return render(request, "admin/edit_photo.html", {
        "lake": lake,
        "photo": photo,
        "form": form,
    })

@login_required
def edit_document(request, lake_id=None, document_id=None):
    """
    The add/edit page for a document. If a document_id is passed in, we edit. If the
    lake_id is passed in, we create
    """
    try:
        document = Document.objects.get(pk=document_id)
        lake = document.lake
    except Document.DoesNotExist:
        # create a new document with a foreign key to the lake
        lake = get_object_or_404(Lake, pk=lake_id)
        document = Document(lake=lake)

    if request.POST:
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document %s" % "Edited" if document_id else "Created")
            return HttpResponseRedirect(reverse("admin-edit-lake", args=(lake.pk,)))
    else:
        form = DocumentForm(instance=document)

    return render(request, "admin/edit_document.html", {
        "lake": lake,
        "document": document,
        "form": form,
    })

@login_required
def  add_plant(request):
    """ 
    This page will have a textbox for user to input plant info,
    which will be delimited by Tab character.
    """
    if request.POST:
        form = PlantForm(request.POST)
        if form.is_valid():
            form.show()
            messages.success(request, " Plants information is saved ")
            return HttpResponseRedirect(reverse("admin-add-plant"))
    else:
        form = PlantForm()

    return render(request, "admin/add_plant.html", {
        "form": form,
    })

    