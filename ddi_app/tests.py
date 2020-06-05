from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ddi_app.models import Test

# Create your tests here.


class TestsTestCase(TestCase):
    fixtures = ['test_fixtures.json']

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_user_1', email='test1@example.com',
                                              password='test_password_1')
        test1 = Test.objects.create(user=user,title='new1test',description='description',attempts=3,
                                    question_min_number=6,complete=False)
        test2 = Test.objects.create(user=user,title='new1test2',description='description2',attempts=2,
                                    question_min_number=5,complete=False)

    def setUp(self):
        self.client = Client()

    def testCreatedTest(self):
        result = self.client.login(username='test_user_1', password='test_password_1')
        self.assertEqual(result, True)

        response = self.client.get(reverse('test_page', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('test_page', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('test_page', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('test_page', kwargs={'pk': 11}))
        self.assertEqual(response.status_code, 200)

