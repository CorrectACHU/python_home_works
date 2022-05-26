from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientRegisterView,
    UserViewList,
    ListCompaniesView,
    DetailCompaniesView,
    ListOrderView,
    CreateOrderView,
    DetailOrderView,
    ListOfferView,
    CreateRatingView,
    ListReviewView,
    CreateCompaniesView
)



urlpatterns = [
    path('register/', ClientRegisterView.as_view()),
    path('users/', UserViewList.as_view()),
    path('companies/', ListCompaniesView.as_view()),
    path('companies/create/', CreateCompaniesView.as_view()),
    path('companies/<int:pk>/', DetailCompaniesView.as_view()),
    path('orders/', ListOrderView.as_view()),
    path('orders/create/', CreateOrderView.as_view()),
    path('orders/<int:pk>', DetailOrderView.as_view()),
    path('offers/', ListOfferView.as_view()),
    path('add_rating/', CreateRatingView.as_view()),
    path('review/', ListReviewView.as_view()),
    path('review/<int:pk>', CreateRatingView.as_view()),

]
