from django.contrib.auth.models import User
from rest_framework import generics, status
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import CompanyUser, Offer, Order

from .serializers import (
    CompanyDetailSerializer,
    CompanySerializer,
    CompanyCreateSerializer,
    CreateOfferSerializer,
    OfferDetailSerializer,
)


class CompanyCreateView(generics.CreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyCreateSerializer


class CompanyProfileView(generics.RetrieveAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyDetailSerializer
    # permission_classes = [CompanyProfileOnly]


class CreateOfferView(generics.ListCreateAPIView):
    serializer_class = CreateOfferSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        company = CompanyUser.objects.get(profile_id=user)
        queryset = Offer.objects.filter(company=company)
        return queryset

    def create(self, request, *args, **kwargs):
        self.order = Order.objects.get(pk=self.request.data['order'])

        if self.order.status != 'open':
            return Response('This order already closed', status=status.HTTP_400_BAD_REQUEST)

        if Offer.objects.filter(company=self.company, order=self.order).exists():
            return Response('This offer already exists', status=status.HTTP_400_BAD_REQUEST)

        return super(CreateOfferView, self).create(request=request)

    def perform_create(self, serializer):
        price = self.order.square_in_meters * self.company.pay_per_hour
        serializer.save(company=self.company, price=price)


#
class OfferDetailView(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
