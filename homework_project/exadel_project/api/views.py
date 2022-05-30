from rest_framework import generics, permissions, views
from django.contrib.auth.models import User

from .permissions import ClientUserOnly
from .serializers import (
    CompanySerializer,
    ComapnyRegisterSerializer,
    OrderSerializer,
    OfferSerializer,
    RatingCompanySerializer, ClientUserSerializer)
from main.models import (
    ClientUser,
    CompanyUser,
    Order,
    Offer,
    RatingCompany,
    Comment,
)
from .services import StandardResultsSetPagination


class ClientUserCreate(generics.CreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer


class ListCompaniesView(generics.ListCreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [ClientUserOnly]


class CreateCompaniesView(generics.CreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = ComapnyRegisterSerializer


class DetailCompaniesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class ListOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ClientUserOnly]


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DetailOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ListOfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class CreateRatingView(generics.CreateAPIView):
    queryset = RatingCompany.objects.all()
    serializer_class = RatingCompanySerializer
    pagination_class = StandardResultsSetPagination


