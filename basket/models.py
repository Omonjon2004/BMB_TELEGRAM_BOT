from django.db import models

from account.models import Users
from orders.models import Product
from shared.models import TimeStampedModel


class Basket(TimeStampedModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Basket of {self.user.username}"


class BasketItem(TimeStampedModel):
    basket = models.ForeignKey('Basket',
                               related_name='items',
                               on_delete=models.CASCADE)
    medication = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)