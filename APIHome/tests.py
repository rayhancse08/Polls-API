from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from APIHome import views
from rest_framework.test import APIClient
# Create your tests here.

class TestPoll(APITestCase):
    def setUp(self):
        self.factory=APIRequestFactory()
        self.view=views.PollViewSet.as_view({'get':'list'})
        self.uri='/polls/'
        self.user=self.setup_user()
    @staticmethod
    def setup_user():
        User=get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_list(self):
        request=self.factory.get(self.uri)
        request.user=self.user
        response=self.view(request)
        self.assertEqual(response.status_code,200)
'''

class TestPoll(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.view = views.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        #self.user = self.setup_user()

    def test_list2(self):
        self.client.login(username="test1", password="test1")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

'''