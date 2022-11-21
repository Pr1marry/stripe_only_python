from django.urls import path
from .views import BuyOrderViewSet, BuyItemViewSet

urlpatterns = [
    path('buy/<int:pk>/', BuyItemViewSet.as_view({'get': 'retrieve'})),
    path('order/<int:pk>/', BuyOrderViewSet.as_view({'get': 'retrieve'})),
]
