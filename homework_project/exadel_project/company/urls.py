from django.urls import path
from .views import (
    CompanyProfileView,
    CompanyCreateView,
)

urlpatterns = [
    path('register/', CompanyCreateView.as_view(), name='company-register'),
    path('profile/<int:pk>/', CompanyProfileView.as_view()),
]