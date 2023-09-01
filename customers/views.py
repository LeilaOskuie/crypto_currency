from decimal import Decimal
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import CustomerSerializer
from .models import Customer

@api_view(["POST"])
def charge_wallet(request):
    customer_id = request.data.get('customer_id')
    amount = request.data.get("amount")

    customer = Customer.objects.get(id=customer_id)

    if not amount:
        return Response({"error": "Please provide an amount to charge."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        customer.wallet_balance += Decimal(amount)
        customer.save()
        return Response({"message": f"The Wallet charged with {amount}."}, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "The amount is not valid"}, status=status.HTTP_400_BAD_REQUEST)
