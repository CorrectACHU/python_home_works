from django.contrib.auth.models import User
from django.db import models
from rest_framework import status, generics

from main.models import (
    ClientUser,
    Comment,
    CompanyUser,
    Order,
    Offer,
    RatingCompany
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .permissions import IsClient, IsOwnerOrReadOnly
from .serializers import (
    ClientDetailSerializer,
    CommentCreateSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer,
    CompanyListSerializer,
    CompanyDetailSerializer,
    OrderListSerializer,
    AnswerToOfferSerializer,
    CloseOrderSerializer,
    AddRatingSerializer
)
from django_filters.rest_framework import DjangoFilterBackend

from .service import CompaniesFilter


class ClientCreateView(generics.CreateAPIView):
    """ Create Client """
    queryset = ClientUser.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [AllowAny]


class ClientProfileView(generics.RetrieveAPIView):
    """ Details about the client profile """
    serializer_class = ClientDetailSerializer
    queryset = ClientUser.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class CreateCommentView(generics.CreateAPIView):
    """ Write a comment to the company """
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsClient]

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))


class CompanyListView(generics.ListAPIView):
    """ Existing companies with filters by rating to them """
    serializer_class = CompanyListSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompaniesFilter

    def get_queryset(self):
        queryset = CompanyUser.objects.all().annotate(
            avg_rating=models.Sum(models.F('evaluations__star_value')) / models.Count(models.F('evaluations'))
        )
        return queryset


class CompanyRetrieveView(generics.RetrieveAPIView):
    """ Details about each company """
    serializer_class = CompanyDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CompanyUser.objects.all().annotate(
            rating_client=models.Count("evaluations", filter=models.Q(evaluations__client_owner=self.request.user.id))
        ).annotate(
            avg_rating=models.Sum(models.F('evaluations__star_value')) / models.Count(models.F('evaluations'))
        )
        return queryset


class AddRatingView(generics.CreateAPIView):
    """ Add rating to the company """
    queryset = RatingCompany.objects.all()
    serializer_class = AddRatingSerializer
    permission_classes = [IsClient]

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))


class CreateOrderView(generics.CreateAPIView):
    """ Create an order """
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [IsClient]

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))


class ListOrderView(generics.ListAPIView):
    """ Personal orders """
    serializer_class = OrderListSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        queryset = Order.objects.filter(client_owner=self.request.user.id)
        return queryset


class RetrieveOrderView(generics.RetrieveUpdateDestroyAPIView):
    """ Details about personal order """
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        serializer.save(client_owner=ClientUser.objects.get(profile=user))


class AnswerToOfferView(generics.UpdateAPIView):
    """ Response to company offers """
    serializer_class = AnswerToOfferSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Order.objects.all().prefetch_related('offer_id')
        return queryset

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        accepted_offers = [offer for offer in obj.offer_id.all() if offer.is_accepted == True]
        list_with_offers_id = [str(offer.id) for offer in obj.offer_id.all()]
        exists_accepted_offer = obj.offer_id.get(id=request.data['accepted_offer']).is_accepted

        if obj.status == 'closed':
            return Response('This order is already closed!', status=status.HTTP_400_BAD_REQUEST)

        if exists_accepted_offer == True:
            return Response('You already answered that way.', status=status.HTTP_400_BAD_REQUEST)

        if len(accepted_offers) > 0:
            c = Offer.objects.filter(id=accepted_offers[0].id)
            c.update(is_accepted=False)

        if not request.data['accepted_offer'] in list_with_offers_id:
            return Response('This object does not exists.', status=status.HTTP_400_BAD_REQUEST)

        offer = Offer.objects.filter(id=int(self.request.data['accepted_offer']))
        offer.update(is_accepted=True)
        return super(AnswerToOfferView, self).put(request=request)

    def perform_update(self, serializer):
        serializer.save(status='in_process')


class CloseOrderView(generics.UpdateAPIView):
    """ Close the personal order """
    queryset = Order.objects.all()
    serializer_class = CloseOrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        obj_queryset = self.queryset.filter(id=obj.id)

        if obj.status == 'closed':
            return Response("This order is already closed!", status=status.HTTP_400_BAD_REQUEST)

        if len(request.data) > 0:
            obj_queryset.update(status='closed')
            return Response('Status was changed!', status=status.HTTP_202_ACCEPTED)

        return Response("Status wasn't changed!", status=status.HTTP_400_BAD_REQUEST)
