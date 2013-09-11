from django.test import TestCase
from django.core.urlresolvers import reverse

class HomeTest(TestCase):
    # just make sure the views return a 200
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_credits(self):
        response = self.client.get(reverse('credits'))
        self.assertEqual(response.status_code, 200)

    def test_map(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)
