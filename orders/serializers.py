from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = [
            "customer",
            "crypto",
            "date_ordered",
            "quantity",
            "total_price",
            "transaction_id",
            "complete"
        ]