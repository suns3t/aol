from django.contrib.gis.db import models

class LakeManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        """
        Override the default query_set for lakes so that the fishing_zone
        and a commas separated list of counties are always attached to the Lake
        object.
        """
        qs = super(LakeManager, self).get_query_set(*args, **kwargs)
        # always tack on the fishing zone, but exclude the geom since that is rarely needed
        qs = qs.select_related("fishing_zone").defer("fishing_zone__the_geom")
        # we want to get a list of the counties each lake belongs to without
        # multiple round-trips to the DB, or Django's stupid prefetch_related
        # method. We build a little subquery, and cleverly tack it onto the
        # queryset. 
        sql = """
        (SELECT 
            lake_county.lake_id, 
            array_to_string(array_agg(county.altname ORDER BY county.altname), ', ') AS counties
        FROM lake_county INNER JOIN county USING(county_id)
        GROUP BY lake_county.lake_id
        ) counties
        """
        qs = qs.extra(
            select={"counties": "counties.counties"},
            tables=[sql],
            where=["counties.lake_id = lake.lake_id"]
        )
        return qs


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
    county_set = models.ManyToManyField('County', through="LakeCounty")

    objects = LakeManager()

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
    name = models.CharField(db_column="altname", max_length=255)
    # includes the "County" suffix
    full_name = models.CharField(db_column="instname", max_length=255)
    the_geom = models.MultiPolygonField(srid=3644)

    class Meta:
        db_table = "county"
        ordering = ["name"]


class LakeCounty(models.Model):
    lake_county_id = models.AutoField(primary_key=True)
    lake = models.ForeignKey("Lake")
    county = models.ForeignKey("County")

    class Meta:
        db_table = "lake_county"
