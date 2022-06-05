from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import (
    CompanyUser,
    Comment,
    Order,
    Offer
)


class UserSerializerCompany(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class CommentSerializer(serializers.ModelSerializer):
    client_id = serializers.SlugRelatedField(
        slug_field='nick',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['notified_companies', 'status']


class CompanyDetailSerializer(serializers.ModelSerializer):
    reviews = CommentSerializer(read_only=True, many=True)
    orders = OrdersSerializer(read_only=True, many=True)

    class Meta:
        model = CompanyUser
        exclude = ['is_company', 'date_create_company']


class CompanyCreateSerializer(serializers.ModelSerializer):
    profile_id = UserSerializerCompany()

    def create(self, validated_data):
        profile_id = User.objects.create(**validated_data['profile_id'])
        profile_id.set_password(validated_data['profile_id']["password"])
        profile_id.save()
        validated_data['profile_id'] = profile_id
        company = super(CompanyCreateSerializer, self).create(validated_data=validated_data)
        company.save()
        return company

    class Meta:
        model = CompanyUser
        exclude = ['is_company']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ['title', 'company_country', 'pay_per_hour']


class CreateOfferSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Offer
        exclude = ['company']


class OfferDetailSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Offer
        exclude = ['order']
