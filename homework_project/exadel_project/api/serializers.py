from django.utils.datetime_safe import datetime
from rest_framework import serializers

from main.models import ClientUser, CompanyUser, Order, Offer, RatingStar, RatingCompany, Review, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'is_active', 'is_superuser']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['user', 'client_country', 'client_city']


class RatingStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingStar
        fields = '__all__'


class RatingCompanySerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=CompanyUser.objects.all())
    rating_owner = serializers.PrimaryKeyRelatedField(queryset=ClientUser.objects.all())
    star_value = serializers.PrimaryKeyRelatedField(queryset=RatingStar.objects.all())

    class Meta:
        model = RatingCompany
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    evaluations = RatingCompanySerializer(many=True, read_only=True)

    class Meta:
        model = CompanyUser
        fields = [
            'id',
            'evaluations',
            'username',
            'email',
            'description',
            'title',
            'company_country',
            'company_city',
            'company_address',
            'pay_per_hour'
        ]


class OfferSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_offer = OfferSerializer(many=True, read_only=True)
    client_owner = serializers.PrimaryKeyRelatedField(queryset=ClientUser.objects.all())

    class Meta:
        model = Order
        exclude = ['status']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
