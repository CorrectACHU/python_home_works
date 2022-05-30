from django.urls import path
from .views import (
    ListCompaniesView,
    DetailCompaniesView,
    ListOrderView,
    CreateOrderView,
    DetailOrderView,
    ListOfferView,
    CreateRatingView,
    CreateCompaniesView,
    ClientUserCreate,
)

urlpatterns = [
    path('register/', ClientUserCreate.as_view()),
    path('companies/', ListCompaniesView.as_view()),
    path('companies/create/', CreateCompaniesView.as_view()),
    path('companies/<int:pk>/', DetailCompaniesView.as_view()),
    path('orders/', ListOrderView.as_view()),
    path('orders/create/', CreateOrderView.as_view()),
    path('orders/<int:pk>', DetailOrderView.as_view()),
    path('offers/', ListOfferView.as_view()),
    path('add_rating/', CreateRatingView.as_view()),
    path('review/<int:pk>', CreateRatingView.as_view()),

]
