from django.contrib.gis.db import models

class Lake(models.Model):
    lake_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField()

    gnis_id = models.CharField(max_length=255)
    gnis_name = models.CharField(max_length=255)
    reachcode = models.CharField(max_length=255, unique=True)

    # the page number of this lake in the original AOL book
    page_number = models.IntegerField(db_column="aol_page")

    fishing_zone = models.ForeignKey('FishingZone')    
    huc6 = models.ForeignKey('HUC6')
    counties = models.ManyToManyField('County', through="LakeCounty")


    class Meta:
        db_table = 'lake'


class FishingZone(models.Model):
    fishing_zone_id = models.AutoField(primary_key=True)
    odfw = models.CharField(max_length=255)
    the_geom = models.MultiPolygonField(srid=3644)

    class Meta:
        db_table = "fishing_zone"


class HUC6(models.Model): 
    huc6_id = models.AutoField(primary_key=True)
    the_geom = models.MultiPolygonField(srid=3644)

    class Meta:
        db_table = "huc6"


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # includes the "County" suffix
    full_name = models.CharField(max_length=255)
    the_geom = models.MultiPolygonField(srid=3644)

    class Meta:
        db_table = "county"


class LakeCounty(models.Model):
    lake_county_id = models.AutoField(primary_key=True)
    lake = models.ForeignKey("Lake")
    county = models.ForeignKey("County")

    class Meta:
        db_table = "lake_county"
