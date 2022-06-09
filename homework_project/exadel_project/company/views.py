from django.contrib.auth.models import User
from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main.models import CompanyUser, Offer, Order

from .permissions import IsCompanyOrReadOnly, IsCompanyProfileOnly, ForUpdateCompanyOnly
from .serializers import (
    CompanyDetailSerializer,
    CompanyCreateSerializer,
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferListSerializer
)


class CompanyCreateView(generics.CreateAPIView):
    """ Create the company """
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = [AllowAny]


class CompanyProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Details about company
    Order notifications
    Change pay_per_hour field
    """
    serializer_class = CompanyDetailSerializer
    permission_classes = [ForUpdateCompanyOnly]

    def get_queryset(self):
        queryset = CompanyUser.objects.all().annotate(
            avg_rating=models.Sum(models.F('evaluations__star_value')) / models.Count(models.F('evaluations'))
        )
        return queryset


class ListOfferView(generics.ListAPIView):
    """ List company offers """
    serializer_class = OfferListSerializer
    permission_classes = [IsCompanyProfileOnly]

    def get_queryset(self):
        queryset = Offer.objects.filter(company=self.request.user.id)
        return queryset


class CreateOfferView(generics.CreateAPIView):
    """ Create an offer for a client order """
    serializer_class = OfferCreateSerializer
    permission_classes = [IsCompanyProfileOnly]

    def get_company(self):
        user = User.objects.get(id=self.request.user.id)
        company = CompanyUser.objects.get(profile_id=user)
        return company

    def get_order(self):
        order = Order.objects.get(pk=self.request.data['order'])
        return order

    def get_queryset(self):
        queryset = Offer.objects.filter(company=self.get_company())
        return queryset

    def create(self, request, *args, **kwargs):
        company = self.get_company()
        order = self.get_order()

        if order.status != 'open':
            return Response('This order already closed', status=status.HTTP_400_BAD_REQUEST)

        if Offer.objects.filter(company=company, order=order).exists():
            return Response('This offer already exists', status=status.HTTP_400_BAD_REQUEST)

        return super(CreateOfferView, self).create(request=request)

    def perform_create(self, serializer):
        company = self.get_company()
        order = self.get_order()
        price = order.square_in_meters * company.pay_per_hour
        serializer.save(company=company, price=price)


#
class OfferDetailView(generics.RetrieveDestroyAPIView):
    """ Details about offer """
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsCompanyProfileOnly]
