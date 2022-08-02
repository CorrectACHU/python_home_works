from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import (
    ClientUser,
    Comment,
    CompanyUser,
    Order,
    Offer,
    RatingCompany
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        ref_name = 'UserClient'


class ClientDetailSerializer(serializers.ModelSerializer):
    profile = UserSerializer()

    def create(self, validated_data):
        profile = User.objects.create(**validated_data['profile'])
        profile.set_password(validated_data['profile']["password"])
        profile.save()
        validated_data['profile'] = profile
        client = super(ClientDetailSerializer, self).create(validated_data=validated_data)
        client.save()
        return client

    class Meta:
        model = ClientUser
        exclude = ['is_client']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['profile']


class CommentCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(queryset=CompanyUser.objects.all())

    class Meta:
        model = Comment
        exclude = ['client_owner']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ['company_id' ,'client_owner']
        ref_name = 'CommentClient'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('client_owner', 'status', 'accepted_offer')


class OfferDetailSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    company = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Offer
        exclude = ['order']
        ref_name = 'OfferClient'


class OrderListSerializer(serializers.ModelSerializer):
    offer_id = OfferDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'head', 'status', 'date_create_order', 'offer_id']


class OrderDetailSerializer(serializers.ModelSerializer):
    offer_id = OfferDetailSerializer(many=True, read_only=True)
    accepted_offer = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'head', 'body', 'accepted_offer', 'notified_companies', 'offer_id']


class CompanyListSerializer(serializers.ModelSerializer):
    profile_id = serializers.SlugRelatedField(slug_field='id', read_only=True)
    avg_rating = serializers.IntegerField()

    class Meta:
        model = CompanyUser
        fields = ['profile_id', 'title', 'pay_per_hour', 'avg_rating']


class CompanyDetailSerializer(serializers.ModelSerializer):
    rating_client = serializers.BooleanField()
    avg_rating = serializers.IntegerField()
    reviews = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = CompanyUser
        fields = [
            'title', 'description', 'company_country', 'company_city', 'date_create_company', 'reviews',
            'rating_client',
            'avg_rating'
        ]
        ref_name = 'CompanySerializerClient'


class AnswerToOfferSerializer(serializers.ModelSerializer):
    head = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)
    offer_id = OfferDetailSerializer(many=True, read_only=True)
    accepted_offer = serializers.CharField()
    square_in_meters = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        exclude = ['client_owner', 'notified_companies', 'country', 'city', 'street', 'house_door']


class CloseOrderSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(help_text='Do you want to close the order?', write_only=True)
    head = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'head', 'body', 'status']


class AddRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingCompany
        exclude = ('client_owner',)
