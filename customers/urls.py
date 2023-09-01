from django.urls import path

from .views import charge_wallet

urlpatterns = [
    path("charge_wallet/", charge_wallet, name="charge_wallet"),
]