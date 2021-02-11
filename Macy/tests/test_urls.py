from django.test import TestCase
from Macy.views import *

"""
    test_urls.py:
    testing routing process through urls.py here. 
"""


class RoutingTests(TestCase):

    def test_get_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_get_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_signup_template_name(self):
        template_name = ['registration/signup.html']
        response = self.client.get('/signup/')
        self.assertEquals(response.template_name, template_name)
