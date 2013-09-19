from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from aol.models import Lake, Photo, Document
from aol.forms.admin import DocumentForm, LakeForm

def listing(request):
    """List all the lakes that the admin can edit"""
    lakes = Lake.objects.all()
    return render(request, "admin/listing.html", {
        "lakes": lakes,
    })

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

    return render(request, "admin/edit_lake.html", {
        "lake": lake,
        "form": form,
    })

