from django.urls import path
from .views import (
    CompanyProfileView,
    CompanyCreateView,
    CreateOfferView,
    ListOfferView,
    OfferDetailView
)

urlpatterns = [
    path('register_company/', CompanyCreateView.as_view(), name='register-company'),
    path('profile_id/<int:pk>/', CompanyProfileView.as_view(), name='company-details'),
    path('offers/', ListOfferView.as_view(), name='list-offers'),
    path('offers/create', CreateOfferView.as_view(), name='create-offer'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail')
]