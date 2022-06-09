from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import (
    ClientUser,
    Comment,
    CompanyUser,
    Order,
    Offer,
)


class UserSerializerClient(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class ClientDetailSerializer(serializers.ModelSerializer):
    profile = UserSerializerClient()

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


class CreateReviewSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=ClientUser.objects.all())
    company_id = serializers.PrimaryKeyRelatedField(queryset=CompanyUser.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # client_id = serializers.SlugRelatedField(slug_field='profile',read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('client_owner', 'status')


class OfferDetailSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    company = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Offer
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    offer_id = OfferDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
