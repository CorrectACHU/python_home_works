from django.urls import path
from .views import (
    ClientProfileView,
    ClientCreateView,
    CreateCommentView,
    CommentView,
    CompanyListView,
    CompanyRetrieveView,
    CreateOrderView,
    RetrieveOrderView,
    ListOrderView,
    AnswerToOfferView,
    CloseOrderView,
    AddRatingView
)

urlpatterns = [
    path('register_client/', ClientCreateView.as_view(), name='client-register'),
    path('profile/<int:pk>/', ClientProfileView.as_view(), name='client-details'),
    path('add_comment/', CreateCommentView.as_view(), name='add-comment'),
    path('add_rating/', AddRatingView.as_view(), name='add-rating'),
    path('reviews/', CommentView.as_view(), name='reviews'),
    path('companies/', CompanyListView.as_view(), name='companies-list'),
    path('companies/<int:pk>/', CompanyRetrieveView.as_view(), name='client-company-details'),
    path('create_order/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', ListOrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', RetrieveOrderView.as_view(), name='order-details'),
    path('orders/<int:pk>/answer', AnswerToOfferView.as_view(), name='offer-answer'),
    path('orders/<int:pk>/close', CloseOrderView.as_view(), name='order-closed')
]
