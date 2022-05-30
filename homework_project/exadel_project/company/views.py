from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import CompanyUser

from .serializers import CompanyDetailSerializer, CompanySerializer, CompanyCreateSerializer


class CompanyCreateView(generics.CreateAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyCreateSerializer


class CompanyProfileView(generics.RetrieveAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyDetailSerializer
    # permission_classes = [CompanyProfileOnly]

