from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Order
from .serializers import OrderListSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]
