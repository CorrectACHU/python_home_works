from rest_framework import serializers
from .models import Order


class OrderListSerializer(serializers.ModelSerializer):
    client_owner = serializers.SlugRelatedField(slug_field='nick', read_only=True)

    class Meta:
        model = Order
        exclude = ['notified_companies', 'street', 'house_door', 'status', 'accepted_offer']
        ref_name = 'OrderForAny'
