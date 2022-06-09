from django.contrib.auth.models import User
from django.db import models
from rest_framework import status, generics

from main.models import (
    ClientUser,
    Comment,
    CompanyUser,
    Order,
    Offer

)
from company.serializers import (
    CompanySerializer
)
from rest_framework.response import Response

from .permissions import ClientProfileOnly, IsClient, ClientOrReadOnly
from .serializers import (
    ClientDetailSerializer,
    CreateReviewSerializer,
    CommentSerializer,
    CreateOrderSerializer,
    OrderSerializer,
    OfferDetailSerializer,

)
from .tasks import count_clients


class ClientCreateView(generics.CreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientDetailSerializer


class ClientProfileView(generics.RetrieveAPIView):
    serializer_class = ClientDetailSerializer
    queryset = ClientUser.objects.all()
    permission_classes = [ClientProfileOnly]


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateReviewSerializer
    permission_classes = [IsClient]


class CommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CompanyListView(generics.ListAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsClient]


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))


class RetrieveOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))

