from django.test import TestCase
from django.core.urlresolvers import reverse
from aol.models import Lake
from ..admin import LakeForm

class LakeFormTest(TestCase):
    fixtures = ['lakes.json']

    def test_form(self):
        lake = Lake.objects.get(title="Matt Lake")
        data = {
            "title": lake.title,
            "body": lake.body,
            "gnis_id": lake.gnis_id,
            "gnis_name": lake.gnis_name,
            "reachcode": lake.reachcode,
            "fishing_zone": lake.fishing_zone.pk,
            "huc6": lake.huc6.pk,
            # set some new counties via their pk
            "county_set": [2, 3]
        }

        form = LakeForm(data, instance=lake)
        self.assertTrue(form.is_valid())
        form.save()
        # make sure the counties got changed in the save method
        self.assertEqual(set(c.pk for c in lake.county_set.all()), set(data['county_set']))
