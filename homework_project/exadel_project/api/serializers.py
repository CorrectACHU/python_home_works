from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import ClientUser, CompanyUser, Order, Offer, RatingStar, RatingCompany, Review, Profile


class UserSerializer(serializers.ModelSerializer):
    is_client = serializers.BooleanField(allow_null=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.is_client = validated_data["is_client"]
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_client']


class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
    class Meta:
        model = CompanyUser
        fields = [
            'description',
            'title',
            'company_country',
            'company_city',
            'company_address',
            'pay_per_hour'
        ]


class ComapnyRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyUser
        fields = [
            'user',
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
