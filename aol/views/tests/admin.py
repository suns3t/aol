from django.test import TestCase
from django.core.urlresolvers import reverse
from aol.models import Lake

class AdminTest(TestCase):
    fixtures = ['lakes.json']

    # just make sure the views return a 200
    def test_listing(self):
        response = self.client.get(reverse('admin-listing'))
        self.assertEqual(response.status_code, 200)

    def test_edit_lake(self):
        lake = Lake.objects.get(title="Matt Lake")
        response = self.client.get(reverse('admin-edit-lake', args=(lake.pk,)))
        self.assertEqual(response.status_code, 200)

        # grab the initial data (which should be valid, and post it back to the form)
        data = response.context['form'].initial
        response = self.client.post(reverse('admin-edit-lake', args=(lake.pk,)), data)
        # the form should be valid, so it should do a redirect
        self.assertEqual(response.status_code, 302)

        # delete a field, thus making the form invalid
        del data['title']
        response = self.client.post(reverse('admin-edit-lake', args=(lake.pk,)), data)
        self.assertFalse(response.context['form'].is_valid())


