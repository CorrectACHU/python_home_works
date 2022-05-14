from django.urls import path
from .views import ListClientsView,ListCompaniesView,api_orders_list, api_order_detail,DetailCompaniesView

urlpatterns = [
    path('clients/', ListClientsView.as_view()),
    path('companies/', ListCompaniesView.as_view()),
    path('companies/<int:pk>/', DetailCompaniesView.as_view()),
    path('orders/', api_orders_list),
    path('orders/<int:pk>/', api_order_detail),
]