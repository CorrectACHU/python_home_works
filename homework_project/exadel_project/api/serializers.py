from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import ClientUser, CompanyUser, Order, Offer, RatingStar, RatingCompany, Review, Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', ]

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: 'Пароль не совпадает'})
        user.set_password(password)
        user.save()
        return user


class ProfileRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


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
    user = ProfileRegisterSerializer()

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
