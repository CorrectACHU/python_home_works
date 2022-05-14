from django.utils.datetime_safe import datetime
from rest_framework import serializers

from main.models import ClientUser, CompanyUser, Order


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    client_country = serializers.CharField(required=False)
    client_city = serializers.CharField(required=False)
    date_create_client = serializers.DateTimeField(default=datetime.utcnow())

    def create(self, validated_data):
        return ClientUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.client_country = validated_data.get('client_country', instance.client_country)
        instance.client_city = validated_data.get('client_city', instance.client_city)
        instance.save()
        return instance


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(max_length=1000)
    email = serializers.EmailField()
    company_country = serializers.CharField()
    company_city = serializers.CharField()
    pay_per_hour = serializers.DecimalField(max_digits=4, decimal_places=2)
    date_create_company = serializers.DateTimeField()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    client_owner = ClientSerializer(serializers.PrimaryKeyRelatedField(queryset=ClientUser.objects.all()), required=False)
    head = serializers.CharField(max_length=50, required=False)
    body = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    square_in_meters = serializers.IntegerField(required=False)
    date_create_order = serializers.DateTimeField(default=datetime.utcnow())

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.client_owner = validated_data.get('client_owner', instance.client_owner)
        instance.head = validated_data.get('head', instance.head)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.square_in_meters = validated_data.get('square_in_meters', instance.square_in_meters)
        instance.save()
        return instance

