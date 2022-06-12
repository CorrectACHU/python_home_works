from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from main.models import ClientUser, CompanyUser, Order, Offer, RatingStar, RatingCompany
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

        """ Create rating stars """
        for x in range(1, 6):
            RatingStar.objects.create(value=x)

    def test_create_client(self):
        """ Test create client view: ClientCreateView"""

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

    def test_get_client_profile(self):
        """ Get client profile -- view: ClientProfileView"""

        response_client1 = self.client1_api.get(
            reverse('client-details', kwargs={'pk': self.client1.profile.id}),
            format='json'
        )
        response_client2 = self.client2_api.get(
            reverse('client-details', kwargs={'pk': self.client2.profile.id}),
            format='json'
        )

        self.assertEqual(response_client1.data['profile']['id'], self.client1.profile.id)
        self.assertEqual(response_client2.data['profile']['id'], self.client2.profile.id)

    def test_create_comment(self):
        """ Test create comment -- view: CreateCommentView"""

        response = self.client1_api.post(
            reverse('add-comment'),
            data={
                'client_owner': self.client1.profile.id,
                'company_id': self.company1.profile_id.id,
                'header': "It's me ad my comment",
                'text': "Hello, it's a nice company"
            })
        self.assertEqual(response.status_code, 201)

    def test_add_rating(self):
        """ Create order -- view: AddRatingView """
        post_rating = self.client1_api.post(
            reverse('add-rating'),
            data={
                'company': self.company1.profile_id.id,
                'star_value': RatingStar.objects.get(value=3).id
            },
            format='json'
        )
        self.assertEqual(post_rating.data['id'], 1)
        self.assertEqual(RatingCompany.objects.get(id=1).company, self.company1)
        self.assertEqual(RatingCompany.objects.get(id=1).client_owner, self.client1)

    def test_companies_list(self):
        """ Return list of companies -- view: CompanyListView'"""

        response = self.client1_api.get(reverse('companies-list'))
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], self.company1.title)

    def test_client_company_details(self):
        """ Return details about company -- view: CompanyRetrieveView"""
        get_company = self.client1_api.get(
            reverse('client-company-details', kwargs={'pk': 3}),
            format='json'
        )
        self.assertEqual(get_company.data['title'], 'CleanF')

    def test_orders_logic(self):
        """ retrieve, list, update, destroy, create Order"""

        """ CREATE ORDERS """
        post_order1 = self.client1_api.post(
            reverse('create-order'),
            data={
                'client_owner': self.client1.profile.id,
                'head': 'Hello, clean my room , pls',
                'body': 'This is so dirty',
                'country': 'Poland',
                'city': 'Poznan',
                'street': 'Ogorodowa',
                'house_door': '20/11',
                'square_in_meters': 20.00,
                'notified_companies': [3, 4]
            },
            format='json'
        )
        post_order2 = self.client2_api.post(
            reverse('create-order'),
            data={
                'client_owner': self.client2.profile.id,
                'head': 'I need help!',
                'body': 'My room so disgusting!',
                'country': 'Poland',
                'city': 'Poznan',
                'street': 'Polanowska',
                'house_door': '1/44',
                'square_in_meters': 29.00,
                'notified_companies': [3, 4]
            },
            format='json'
        )

        """ CREATE OFFERS """
        notifies_company1 = [order['id'] for order in self.company1.orders.values()]
        notifies_company2 = [order['id'] for order in self.company2.orders.values()]

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

        """ GET OFFERS """
        get_order1 = self.client1_api.get(
            reverse('order-details', kwargs={'pk': 1}),
            format='json'
        )
        offers_order1 = [offer['id'] for offer in get_order1.data['offer_id']]

        get_order2 = self.client2_api.get(
            reverse('order-details', kwargs={'pk': 2}),
            format='json'
        )
        offers_order2 = [offer['id'] for offer in get_order2.data['offer_id']]

        """ ANSWER TO OFFER """
        self.client1_api.put(
            reverse('offer-answer', kwargs={'pk': 1}),
            data={
                "accepted_offer": str(offers_order1[0])
            },
            format='json'
        )
        self.client2_api.put(
            reverse('offer-answer', kwargs={'pk': 2}),
            data={
                "accepted_offer": str(offers_order2[1])
            },
            format='json'
        )

        """ CLOSE ORDER """
        self.client1_api.put(
            reverse('order-closed', kwargs={'pk': 1}),
            data={
                'status': True
            },
            format='json'
        )
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=1).status, 'closed')
        self.assertEqual(Order.objects.get(id=2).status, 'in_process')
        self.assertEqual(Offer.objects.get(id=1).is_accepted, True)
        self.assertEqual(Offer.objects.get(id=4).is_accepted, True)
        self.assertEqual(Offer.objects.get(id=2).is_accepted, False)
        self.assertEqual(Offer.objects.get(id=3).is_accepted, False)
