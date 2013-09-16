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

    def test_search_lake(self):
        '''test that a blank query returns all lakes'''
        lakes = list(Lake.objects.all())
        response = self.client.get("%s?q=%s" % (reverse('lakes-search'), "") )
        self.assertEqual(len(lakes), response.context['lakes'].count())
 
    def test_lake_search_title(self):
        '''test lake title query returns lake page assumes unique ttile which is true of test data'''
        lakes = list(Lake.objects.all())
        # test the first couple lakes
        for lake in lakes:
            response = self.client.get("%s?q=%s" % (reverse('lakes-search'), lake.title) )
            #test that you get redirected
            self.assertEqual(response.status_code, 302)
            #check if reachcode is in redirect url
            self.assertIn(lake.reachcode,str(response))
    
    def test_lake_search_garbage(self):
        '''test garbage query returns error/no results'''
        response = self.client.get("%s?q=fhsy78rh" % reverse('lakes-search'))
        #test context contains error
        self.assertIn('error', response.context)
        self.assertEqual(response.status_code, 200)
