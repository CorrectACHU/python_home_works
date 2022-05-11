from django.shortcuts import render
from rest_framework import generics, status

from .serializers import ClientSerializer, CompanySerializer, OrderSerializer
from main.models import ClientUser, CompanyUser, Order
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ListClientsView(generics.ListCreateAPIView):
    queryset = ClientUser.objects.all()
    serializer_class = ClientSerializer


class ListCompaniesView(generics.ListAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


class DetailCompaniesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanySerializer


@api_view(['GET', 'POST'])
def api_orders_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def api_order_detail(request, pk):
    try:
        order = Order.objects.select_related('client_owner').get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
