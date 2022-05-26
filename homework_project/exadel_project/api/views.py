from django.db import models
from rest_framework import generics, permissions, views
from django.contrib.auth.models import User
from rest_framework.response import Response
from .permissions import ClientPermissionOrReadOnly, ClientPermission
from .serializers import (
    UserSerializer,
    UserSerializerList,
    CompanySerializer,
    ComapnyRegisterSerializer,
    OrderSerializer,
    OfferSerializer,
    ReviewSerializer,
    RatingCompanySerializer)
from main.models import (
    ClientUser,
    CompanyUser,
    Order,
    Offer,
    RatingCompany,
    Review,
    Profile)
from .services import StandardResultsSetPagination


class ClientRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self,request,*args,**kwargs):
        client = User.objects.annotate(is_client=True)
        return client


class UserViewList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerList


class ListCompaniesView(generics.ListCreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class CreateCompaniesView(generics.CreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = ComapnyRegisterSerializer


class DetailCompaniesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class ListOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ClientPermissionOrReadOnly]


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ClientPermissionOrReadOnly]


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


class ListReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination


class DetailReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
