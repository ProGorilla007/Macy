from django.test import TestCase
from Macy.tests.factories import UserFactory, LinksFactory

"""
    test_models.py:
    testing model creation, updating, deletion through models.py here. 
"""


class DataCreationTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory(username="tamako")
        self.links = LinksFactory(user_id=self.user2)

    def test_user_created(self):
        self.assertEqual("tamako", self.user2.username)

    def test_links_created(self):
        self.assertEqual(self.user2, self.links.user_id)
