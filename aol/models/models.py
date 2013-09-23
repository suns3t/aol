import os
import re
from PIL import Image
from django.conf import settings as SETTINGS
from django.contrib.gis.db import models

class Document(models.Model):
    """
    Stores all the documents attached to a lake like PDFs, and whatever else an
    admin wants to upload (except Photos which are handled in their own model)
    """
    DOCUMENT_DIR = "pages/"

    document_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=lambda instance, filename: instance.DOCUMENT_DIR + filename)
    rank = models.IntegerField(help_text="The order this field is displayed on the lakes detail page")
    uploaded_on = models.DateTimeField(auto_now_add=True)

    lake = models.ForeignKey('Lake')

    class Meta:
        db_table = 'document'
        ordering = ['rank']


class Photo(models.Model):
    """Stores all the photos attached to a lake"""
    PHOTO_DIR = "photos/"
    THUMBNAIL_PREFIX = "thumbnail-"

    photo_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=lambda instance, filename: instance.PHOTO_DIR + filename, db_column="filename")
    taken_on = models.DateField(null=True, db_column="photo_date")
    author = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)

    lake = models.ForeignKey('Lake')

    class Meta:
        db_table = "photo"

    @property
    def url(self):
        """Returns the complete path to the photo from MEDIA_URL"""
        return self.file.url

    @property
    def thumbnail_url(self):
        """Returns the complete path to the photo's thumbnail from MEDIA_URL"""
        return SETTINGS.MEDIA_URL + os.path.relpath(self._thumbnail_path, SETTINGS.MEDIA_ROOT)

    @property
    def _thumbnail_path(self):
        """Returns the abspath to the thumbnail file, and generates it if needed"""
        filename = self.THUMBNAIL_PREFIX + os.path.basename(self.file.name)
        path = os.path.join(os.path.dirname(self.file.path), filename)
        try:
            open(path).close()
        except IOError:
            self._generate_thumbnail(path)

        return path

    def _generate_thumbnail(self, save_to_location):
        """Generates a thumbnail and saves to to the save_to_location"""
        SIZE = (400, 300)
        im = Image.open(self.file.path)
        im.thumbnail(SIZE, Image.ANTIALIAS)
        im.save(save_to_location)


class DeferGeomManager(models.Manager):
    """
    Models that use this manager will always defer the "the_geom" column. This
    is necessary because the geom columns are huge, and rarely need to be
    accessed.
    """
    def get_query_set(self, *args, **kwargs):
        qs = super(DeferGeomManager, self).get_query_set(*args, **kwargs).defer("the_geom")
        return qs


class FishingZone(models.Model):
    fishing_zone_id = models.AutoField(primary_key=True)
    odfw = models.CharField(max_length=255)
    the_geom = models.MultiPolygonField(srid=3644)

    objects = DeferGeomManager()

    class Meta:
        db_table = "fishing_zone"

    def __unicode__(self):
        return self.odfw


class HUC6(models.Model): 
    huc6_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_column="hu_12_name")
    the_geom = models.MultiPolygonField(srid=3644)

    objects = DeferGeomManager()

    class Meta:
        db_table = "huc6"

    def __unicode__(self):
        return self.name


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column="altname", max_length=255)
    # includes the "County" suffix
    full_name = models.CharField(db_column="instname", max_length=255)
    the_geom = models.MultiPolygonField(srid=3644)

    objects = DeferGeomManager()

    class Meta:
        db_table = "county"
        ordering = ["name"]

    def __unicode__(self):
        return self.full_name

# import all the lakes models into this module
from lakes import *
