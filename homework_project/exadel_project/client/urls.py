from django.urls import path
from .views import (
    ClientProfileView,
    ClientCreateView,
    CreateCommentView,
    CommentView,
    CompanyListView,
)

urlpatterns = [
    path('register/', ClientCreateView.as_view(), name='client-register'),
    path('profile/<int:pk>/', ClientProfileView.as_view()),
    path('add_comment/', CreateCommentView.as_view(), name='add-comment'),
    path('reviews/', CommentView.as_view(), name='reviews'),
    path('companies/', CompanyListView.as_view(), name='companies-list'),
]
