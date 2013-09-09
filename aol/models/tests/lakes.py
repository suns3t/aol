from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from ..models import Lake, FishingZone, County, HUC6, LakeCounty

class LakeTest(TestCase):
    def setUp(self):
        # the geometry doesn't really matter
        the_geom = GEOSGeometry("MULTIPOLYGON (((30 20, 10 40, 45 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))")

        # create a few FishingZones
        fz_ne = FishingZone(odfw="Northeast", the_geom=the_geom)
        fz_ne.save()
        fz_se = FishingZone(odfw="Southeast", the_geom=the_geom)
        fz_se.save()
        fz_nw = FishingZone(odfw="Northwest", the_geom=the_geom)
        fz_nw.save()
        fz_sw = FishingZone(odfw="Southwest", the_geom=the_geom)
        fz_sw.save()

        # create some counties
        clark = County(name="Clark", full_name="Clark County", the_geom=the_geom)
        clark.save()
        washington = County(name="Washington", full_name="Washington County", the_geom=the_geom)
        washington.save()
        foobar = County(name="Foobar", full_name="Foobar County", the_geom=the_geom)
        foobar.save()

        # create some HUCS
        huc_a = HUC6(the_geom=the_geom)
        huc_a.save()
        huc_b = HUC6(the_geom=the_geom)
        huc_b.save()
        huc_c = HUC6(the_geom=the_geom)
        huc_c.save()

        # create some lakes
        matt_lake = Lake(title="Matt Lake", body="This is Matt's Lake", gnis_id="123", gnis_name="Matt Lake", reachcode="123", page_number=1, fishing_zone=fz_nw, huc6=huc_a)
        matt_lake.save()

        foo_lake = Lake(title="Foo Lake", body="This is Foo's Lake", gnis_id="124", gnis_name="Foo Lake", reachcode="124", page_number=2, fishing_zone=fz_sw, huc6=huc_b)
        foo_lake.save()

        bar_lake = Lake(title="bar Lake", body="This is bar's Lake", gnis_id="125", gnis_name="bar Lake", reachcode="125", page_number=3, fishing_zone=fz_sw, huc6=huc_c)
        bar_lake.save()

        # attach the counties to the lake

        # matt_lake spans two counties
        LakeCounty(lake=matt_lake, county=clark).save()
        LakeCounty(lake=matt_lake, county=washington).save()

        LakeCounty(lake=foo_lake, county=washington).save()
        LakeCounty(lake=bar_lake, county=foobar).save()


    def test_get_query_set(self):
        lake = Lake.objects.get(title="Matt Lake")
        # the lake should have the fishing zone set, and not require a query
        with self.assertNumQueries(0):
            self.assertEqual(lake.fishing_zone.odfw, "Northwest")

        # the lake should have a comma separated list of counties
        with self.assertNumQueries(0):
            # the ordering matters here. It's alphabetical
            self.assertTrue(lake.counties, "Clark, Washington")
