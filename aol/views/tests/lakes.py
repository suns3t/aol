from django.test import TestCase
from django.core.urlresolvers import reverse
from aol.models import Lake

class LakesTest(TestCase):
    fixtures = ['lakes.json']

	# just make sure the views return a 200
    def test_listing(self):
        response = self.client.get(reverse('lakes-listing'))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        lakes = list(Lake.objects.all())
        # test the first couple lakes
        for lake in lakes:
            response = self.client.get(reverse('lakes-detail'), kwargs={"reachcode": lake.reachcode})
            self.assertEqual(response.status_code, 200)

    def test_search(self):
        crater = 'crater'
        lakes = list(Lake.objects.all())
        for lake in lakes:
            print lake.title
        response = self.client.get(reverse('lakes-search'), args=crater)
        self.assertIn(crater,response.content)


