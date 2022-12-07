from django.db import models

from .book import Book
from account.models import CustomUser


class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return str(self.customer.username)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.book} {self.quantity}'

    @property
    def get_total(self):
        total = self.book.price * self.quantity
        return total
