from django.urls import path

from .views import base_view, ListClientView, DetailUserView, CompaniesView, AllUsersView, crud_operations


urlpatterns = [
    path('', base_view),
    path('users/', ListClientView.as_view()),
    path('users/<int:pk>/', DetailUserView.as_view()),
    path('companies/', CompaniesView.as_view()),
    path('all_users/', AllUsersView.as_view()),
    path('CRUD/', crud_operations),
]
