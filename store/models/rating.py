from django.db import models
from django.db.models import UniqueConstraint

from account.models import CustomUser
from .book import Book
from store.fields import IntegerRangeField


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = IntegerRangeField(min_value=1, max_value=5, default=2)

    def __str__(self):
        return f"{self.book} : {self.rating}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'book'], name='rating_once')
        ]
