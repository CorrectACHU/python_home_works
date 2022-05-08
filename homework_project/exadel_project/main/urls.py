from django.contrib import admin
from django.urls import path, include

from .views import base_view, ListClientView, DetailUserView, CompaniesView, AllUsersView

urlpatterns = [
    path('', base_view),
    path('users/', ListClientView.as_view()),
    path('users/<int:pk>/', DetailUserView.as_view()),
    path('companies/', CompaniesView.as_view()),
    path('all_users/', AllUsersView.as_view()),
]
