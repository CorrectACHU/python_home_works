from rest_framework import generics

from .models import Order
from .serializers import OrderListSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.filter(status='open')
    serializer_class = OrderListSerializer
