from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from ..models import Lake, FishingZone, County, HUC6, LakeCounty

class LakeTest(TestCase):
    fixtures = ['lakes.json']

    def test_get_query_set(self):
        lake = Lake.objects.get(title="Matt Lake")
        # the lake should have the fishing zone set, and not require a query
        with self.assertNumQueries(0):
            self.assertEqual(lake.fishing_zone.odfw, "Northwest")

        # the lake should have a comma separated list of counties
        with self.assertNumQueries(0):
            # the ordering matters here. It's alphabetical
            self.assertTrue(lake.counties, "Clark, Washington")

    def test_watershed_tile_url(self):
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.watershed_tile_url
        self.assertTrue("?bbox=-295,-295,345,340" in url)

    def test_basin_tile_url(self):
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.basin_tile_url
        self.assertTrue("?bbox=-995,-995,1045,1040" in url)
