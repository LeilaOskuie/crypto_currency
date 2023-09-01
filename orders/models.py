from django.db import models

from customers.models import Customer
from cryptoCurrency.models import CryptoCurrency


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)


