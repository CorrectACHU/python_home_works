from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import ClientUser, CompanyUser, Order, Offer


class ClientTest(APITestCase):
    def setUp(self):
        """ User instances """
        self.user1 = User.objects.create_user(username='johny', password='Eachother1')
        self.user2 = User.objects.create_user(username='Byton', password='Eachother1')
        self.user3 = User.objects.create_user(username='Clean_Factory', password='Eachother1')
        self.user4 = User.objects.create_user(username='Clean&co', password='Eachother1')

        """ Give them tokens """
        self.user1_token = TokenObtainPairSerializer.get_token(user=self.user1).access_token
        self.user2_token = TokenObtainPairSerializer.get_token(user=self.user2).access_token
        self.user3_token = TokenObtainPairSerializer.get_token(user=self.user3).access_token
        self.user4_token = TokenObtainPairSerializer.get_token(user=self.user4).access_token

        """ Create clients """
        self.client1 = ClientUser.objects.create(profile=self.user1, nick='J1a1')
        self.client2 = ClientUser.objects.create(profile=self.user2, nick='B1a1')

        """ Create companies """
        self.company1 = CompanyUser.objects.create(
            profile_id=self.user3,
            title='CleanF',
            description='This company was made on 1231',
            phone='+48444333222',
            company_country='Poland',
            company_city='Poznan',
            company_address='Ogorodowa 9',
            pay_per_hour=12.00,
        )
        self.company2 = CompanyUser.objects.create(
            profile_id=self.user4,
            title='CoF',
            description='This company was made on 23231',
            phone='+48424333222',
            company_country='Poland',
            company_city='Poznan',
            company_address='Browarska 9',
            pay_per_hour=10.00,
        )

        """ Log in clients """
        self.client1_api = APIClient()
        self.client1_api.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user1_token))
        self.client2_api = APIClient()
        self.client2_api.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user2_token))

        """ Log in companies """
        self.company1_api = APIClient()
        self.company1_api.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user3_token))
        self.company2_api = APIClient()
        self.company2_api.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user4_token))

        """ Orders """
        self.order1 = Order.objects.create(
            client_owner=self.client1,
            head='Hello, clean my room , pls',
            body='This is so dirty',
            country='Poland',
            city='Poznan',
            street='Ogorodowa',
            house_door='20/11',
            square_in_meters=20.00
        )
        self.order1.notified_companies.set([3, 4])

        self.order2 = Order.objects.create(
            client_owner=self.client2,
            head='clean my room',
            body='Faster faster',
            country='Poland',
            city='Poznan',
            street='Ptasia',
            house_door='19/2',
            square_in_meters=12.50
        )
        self.order2.notified_companies.set([3, 4])

    def test_create_company(self):
        """ Test create company """

        client = APIClient()
        response = client.post(
            reverse('register-company'),
            data={
                'profile_id': {
                    'username': 'CompanyFast',
                    'password': 'Eachother1',
                    'email': 'jabsssss@gmail.com'
                },
                'title': 'CoFt',
                'description': 'Fast and clean',
                'phone': '+48888555444',
                'company_country': 'Poland',
                'company_city': 'Poznan',
                'company_address': 'Grundwalska 14',
                'pay_per_hour': 14.50,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CompanyUser.objects.get(title='CoFt').pay_per_hour, 14.50)

    def test_get_company_profile(self):
        """ Return company details """
        get_company1 = self.company1_api.get(
            reverse('company-details', kwargs={'pk': self.company1.profile_id.id}),
            format='json'
        )
        get_company2 = self.company2_api.get(
            reverse('company-details', kwargs={'pk': self.company2.profile_id.id}),
            format='json'
        )
        self.assertEqual(get_company1.data['title'], self.company1.title)
        self.assertEqual(get_company2.data['title'], self.company2.title)

    def test_put_company_profile(self):
        """ Update company details"""
        put_company1 = self.company1_api.put(
            reverse('company-details', kwargs={'pk': self.company1.profile_id.id}),
            data={'pay_per_hour': 25.00},
            format='json'
        )
        put_company2 = self.company2_api.put(
            reverse('company-details', kwargs={'pk': self.company2.profile_id.id}),
            data={'pay_per_hour': 13.00},
            format='json'
        )
        self.assertEqual(put_company1.data['pay_per_hour'],
                         str(CompanyUser.objects.get(title=self.company1.title).pay_per_hour))
        self.assertEqual(put_company2.data['pay_per_hour'],
                         str(CompanyUser.objects.get(title=self.company2.title).pay_per_hour))

    def test_offers(self):
        """ Company Notices """
        notifies_company1 = [order['id'] for order in self.company1.orders.values()]
        notifies_company2 = [order['id'] for order in self.company2.orders.values()]

        """ Create offer """
        self.company1_api.post(
            reverse('create-offer'),
            data={'order': notifies_company1[0]},
            format='json'
        )
        self.company1_api.post(
            reverse('create-offer'),
            data={'order': notifies_company1[1]},
            format='json'
        )
        self.company2_api.post(
            reverse('create-offer'),
            data={'order': notifies_company2[0]},
            format='json'
        )
        self.company2_api.post(
            reverse('create-offer'),
            data={'order': notifies_company2[1]},
            format='json'
        )

        """ Answers to offers by client """
        order1_offers = [offer['id'] for offer in Order.objects.get(id=1).offer_id.values()]
        order2_offers = [offer['id'] for offer in Order.objects.get(id=2).offer_id.values()]

        self.client1_api.put(
            reverse('offer-answer', kwargs={'pk': 1}),
            data={
                'accepted_offer': order1_offers[1]
            }
        )

        self.client2_api.put(
            reverse('offer-answer', kwargs={'pk': 2}),
            data={
                'accepted_offer': order2_offers[0]
            }
        )

        self.assertEqual(Offer.objects.count(), 4)
        self.assertEqual(len(self.company1.orders.values()), 2)
        self.assertEqual(len(self.company2.orders.values()), 2)
        self.assertEqual(Order.objects.get(id=1).accepted_offer, 3)
        self.assertEqual(Order.objects.get(id=2).accepted_offer, 2)
