from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import (
    CompanyUser,
    Comment,
    Order,
    Offer
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        ref_name = 'UserCompany'


class CommentSerializer(serializers.ModelSerializer):
    client_id = serializers.SlugRelatedField(
        slug_field='nick',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        ref_name = 'CommentCompany'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['notified_companies', 'client_owner', 'accepted_offer']


class CompanyDetailSerializer(serializers.ModelSerializer):
    avg_rating = serializers.IntegerField(read_only=True)
    reviews = CommentSerializer(read_only=True, many=True)
    title = serializers.CharField(read_only=True)
    company_country = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    company_city = serializers.CharField(read_only=True)

    class Meta:
        model = CompanyUser
        fields = [
            'title', 'description', 'company_country', 'company_city', 'date_create_company', 'pay_per_hour', 'reviews',
            'avg_rating'
        ]


class CompanyCreateSerializer(serializers.ModelSerializer):
    profile_id = UserSerializer()

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


class OfferListSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field='head', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Offer
        fields = ['order', 'price', 'is_accepted']


class OfferCreateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Offer
        exclude = ['company', 'is_accepted']


class OfferDetailSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Offer
        exclude = ['order']
        ref_name = 'OfferCompany'
