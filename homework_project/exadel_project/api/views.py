from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets, views
from .permissions import ClientPermissionOrReadOnly, ClientPermission
from .serializers import ClientSerializer, \
    CompanySerializer, \
    OrderSerializer, \
    OfferSerializer, \
    RatingCompanySerializer, \
    ReviewSerializer, \
    CustomUserSerializer
from main.models import ClientUser, CompanyUser, Order, Offer, RatingCompany, Review, CustomUser
from .services import StandardResultsSetPagination


class CustomUserViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ListClientsView(generics.ListCreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ClientPermissionOrReadOnly]


class DetailClientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientSerializer


class ListCompaniesView(generics.ListCreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class DetailCompaniesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class ListOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


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


class ListReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination


class DetailReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ViewApi(views.APIView):
#     def get(self, request):
#         queryset = ClientUser.objects.all()
#         serializer = ClientSerializer(queryset, many=True)
#         print((request.user.client_user))
#         return Response(serializer.data)
