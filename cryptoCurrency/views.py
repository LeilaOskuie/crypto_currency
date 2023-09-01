from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CryptoCurrency
from .serializers import CryptoSerializer


class CryptoListAPIView(generics.ListAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]


class CryptoDetailAPIView(generics.RetrieveAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]


class CurrencyCreateView(generics.CreateAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]
