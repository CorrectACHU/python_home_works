from rest_framework import status, generics

from main.models import ClientUser, Comment, CompanyUser
from company.serializers import CompanySerializer

from .permissions import ClientProfileOnly, IsClient, ClientOrReadOnly
from .serializers import ClientDetailSerializer, CreateReviewSerializer, CommentSerializer


class ClientCreateView(generics.CreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientDetailSerializer


class ClientProfileView(generics.RetrieveAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientDetailSerializer
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
