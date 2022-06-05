from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from main.models import ClientUser, CompanyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .tasks import count_clients


class ClientTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='johny', password='Eachother1')
        self.user1.save()
        self.user2 = User.objects.create_user(username='Byton', password='Eachother1')
        self.user2.save()
        self.user3 = User.objects.create_user(username='Clean_Factory', password='Eachother1')
        self.user3.save()
        self.user4 = User.objects.create_user(username='Clean&co', password='Eachother1')
        self.user4.save()

        self.user1_token = TokenObtainPairSerializer.get_token(user=self.user1).access_token
        self.user2_token = TokenObtainPairSerializer.get_token(user=self.user2).access_token

        self.client1 = ClientUser.objects.create(profile=self.user1, nick='J1a1')
        self.client1.save()
        self.client2 = ClientUser.objects.create(profile=self.user2, nick='B1a1')
        self.client2.save()

        self.company1 = CompanyUser.objects.create(profile_id=self.user3, title='CleanF')
        self.company1.save()
        self.company2 = CompanyUser.objects.create(profile_id=self.user4, title='CoF')
        self.company2.save()

    def test_create_client(self):
        client = APIClient()
        response = client.post(
            reverse('client-register'),
            data={
                'profile': {
                    'username': 'Portugalec',
                    'password': 'Eachother1',
                    'email': 'jabomba@gmail.com'
                },
                'nick': 'Harry',
                'name': 'Potter',
                'client_country': 'Poland',
                'client_city': 'Poznan'
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_company(self):
        client = APIClient()
        response = client.post(
            reverse('company-register'),
            data={
                'profile_id': {
                    'username': 'CompanyFast',
                    'password': 'Eachother1',
                    'email': 'jabsssss@gmail.com'
                },
                'title': 'CoFt',
                'description': 'Fast and clean',
                'company_country': 'Poland',
                'company_city': 'Poznan'
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_companies_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user1_token))
        response = client.get(reverse('companies-list'))
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], self.company1.title)

    def test_create_comment(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user1_token))
        response = client.post(
            reverse('add-comment'),
            data={
                'client_id': self.client1.profile.id,
                'company_id': self.company1.profile_id.id,
                'header': "It's me ad my comment",
                'text': "Hello, it's a nice company"
            })
        self.assertEqual(response.status_code, 201)

    def test_celery(self):
        s = count_clients
        self.assertEqual(s(), (2, 'ssssssssssssssssssss'))
