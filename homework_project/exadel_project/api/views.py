from django.contrib.auth.models import User
from rest_framework import generics, permissions, views
from rest_framework.response import Response
from django.db.models.fields import related_descriptors
from .permissions import ClientPermissionOrReadOnly, ClientPermission
from .serializers import ClientSerializer, \
    CompanySerializer, \
    OrderSerializer, \
    OfferSerializer, \
    RatingCompanySerializer, \
    ReviewSerializer, ComapnyRegisterSerializer
from main.models import ClientUser, CompanyUser, Order, Offer, RatingCompany, Review
from .services import StandardResultsSetPagination


class ListClientsView(generics.ListCreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ClientPermissionOrReadOnly]


class DetailClientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ClientPermissionOrReadOnly]


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


class ViewApi(views.APIView):
    def get(self, request):
        queryset = ClientUser.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        print(request.user.client)
        return Response(serializer.data)
