from django.urls import path
from .views import CryptoListAPIView, CryptoDetailAPIView, CurrencyCreateView

urlpatterns = [
    path('crypto/', CryptoListAPIView.as_view(), name='crypto-list'),
    path('crypto/<int:pk>/', CryptoDetailAPIView.as_view(), name='crypto-detail'),
    path('crypto/create/', CurrencyCreateView.as_view(), name='crypto-create'),
    ]