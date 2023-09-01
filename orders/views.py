import datetime
from decimal import Decimal
import uuid

from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from cryptoCurrency.models import CryptoCurrency
from .models import Order
from .tasks import buy_from_exchange


class OrderView(APIView):
    @transaction.atomic
    def post(self, request):
        customer_id = request.data.get("customer_id")
        crypto_id = request.data.get("crypto_id")
        quantity = request.data.get("quantity")
        try:
            quantity = int(quantity)
        except TypeError:
            return Response({"Incorrect input format, the quantity should be int"}, status=status.HTTP_400_BAD_REQUEST)

        crypto_instance = CryptoCurrency.objects.get(id=crypto_id)
        customer_instance = Customer.objects.get(id=customer_id)

        if crypto_id is None:
            return Response({"Incorrect input format, crypto_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if quantity is None or quantity < 1:
            return Response({"Incorrect input format, quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        cost = crypto_instance.price * Decimal(quantity)

        if customer_instance.wallet_balance < cost:
            return Response({"Please charge your account first, the balance is not enough"}, status=status.HTTP_400_BAD_REQUEST)

        # update customer account
        customer_instance.wallet_balance -= cost
        customer_instance.save()

        # insert order
        transaction_id = uuid.uuid4()
        order_instance = Order(
            customer=customer_instance,
            crypto=crypto_instance,
            date_ordered=datetime.datetime.now(),
            complete=False,
            transaction_id=transaction_id,
            quantity=quantity,
            total_price=cost,
        )
        order_instance.save()
        if cost > 10:
            buy_from_exchange.delay(crypto_instance.name, cost)
        else:
            with transaction.atomic():
                none_completed_orders = Order.objects.select_for_update().filter(crypto_id=crypto_id, complete=False)
                total_price_agg = none_completed_orders.aggregate(Sum("total_price"))["total_price__sum"]

                if total_price_agg > 10:
                    buy_from_exchange.delay(crypto_instance.name, total_price_agg)
                    none_completed_orders.update(complete=True)

        return Response({"success": True, "transaction_id": transaction_id})

