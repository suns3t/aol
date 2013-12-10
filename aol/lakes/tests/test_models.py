import os
from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings as SETTINGS
from ..models import Lake, FishingZone, County, HUC6, LakeCounty, Photo

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
        # just make sure the URL has a bbox set in it
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.watershed_tile_url
        self.assertTrue("?bbox=-295,-295,345,340" in url)

    def test_basin_tile_url(self):
        # just make sure the URL has a bbox set in it
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.basin_tile_url
        self.assertTrue("?bbox=-995,-995,1045,1040" in url)

    def test_to_kml(self):
        # make sure invalid scales raise errors
        invalid_scale = 12
        self.assertRaises(ValueError, Lake.objects.to_kml, scale=invalid_scale, bbox=())

        lakes = Lake.objects.to_kml(scale=108000, bbox=(-50000, -50000, 50000, 50000))
        for lake in lakes:
            # make sure the lake has a kml attribute set
            self.assertTrue(lake.kml)

    def test_page_urls(self):
        lake = Lake.objects.get(title="Matt Lake")

        # create the path to the dummy pages
        map_path = os.path.join(SETTINGS.MEDIA_ROOT, "pages", "1_map.pdf")
        page_path = os.path.join(SETTINGS.MEDIA_ROOT, "pages", "1_page.pdf")
        map_url = "/media/pages/1_map.pdf"
        page_url = "/media/pages/1_page.pdf"

        # first, remove the files if they exist (so we are in a known state for this test)
        for path in [map_path, page_path]:
            try:
                os.remove(path)
            except OSError:
                pass

        # `matt lake` doesn't have any pdf pages
        self.assertFalse(lake.page_urls)

        # now create the pdf pages
        open(page_path, 'w').close()
        open(map_path, 'w').close()

        self.assertEqual(lake.page_urls['map'], map_url)
        self.assertEqual(lake.page_urls['page'], page_url)
        self.assertFalse('survey' in lake.page_urls)
        self.assertFalse('stats' in lake.page_urls)


class PhotoTest(TestCase):
    fixtures = ['lakes.json']

    def test_url(self):
        # make sure the URL path is valid
        photo = Photo.objects.get(pk=1)
        self.assertEqual(photo.url, "/media/photos/test.jpg")

    def test_thumbnail_url(self):
        photo = Photo.objects.get(pk=1)

        # delete the thumbnail file
        thumb_path = SETTINGS.ROOT('media', 'photos', 'thumbnail-test.jpg')
        thumb_url = "/media/photos/thumbnail-test.jpg"
        try:
            os.remove(thumb_path)
        except OSError:
            pass

        # this should generate a thumbnail
        self.assertEqual(photo.thumbnail_url, thumb_url)
        # make sure the thumbnail file actually exists
        self.assertTrue(os.path.exists(thumb_path))

        # now we want to make sure subsequent calls to the thumbnail_url do not
        # recreate the image (since that would be expensive)

        # overwrite the file
        flag_text = "this should not be overwritten!"
        with open(thumb_path, 'w') as f:
            f.write(flag_text)
        # try getting the thumbnail URL again
        self.assertEqual(photo.thumbnail_url, thumb_url)
        # make sure it didn't recreate the thumbnail
        with open(thumb_path) as f:
            self.assertEqual(f.read(), flag_text)

        # delete the thumbnail file
        try:
            os.remove(thumb_path)
        except OSError:
            pass
