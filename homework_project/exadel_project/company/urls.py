from django.urls import path
from .views import (
    CompanyProfileView,
    CompanyCreateView,
    # CreateOfferView,
    OfferDetailView
)

urlpatterns = [
    path('register_company/', CompanyCreateView.as_view(), name='company-register'),
    path('profile_id/<int:pk>/', CompanyProfileView.as_view()),
    # path('offers/', CreateOfferView.as_view()),
    path('offers/<int:pk>/', OfferDetailView.as_view())
]