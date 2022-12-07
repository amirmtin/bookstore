from django.db import models
from django_extensions.db.fields import AutoSlugField

from .category import Category
from .author import Author


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
    description = models.TextField()
    pages = models.PositiveIntegerField()
    edition = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    publisher = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='book_pics')
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)

    @property
    def rating_average(self):
        return self.rating.aggregate(models.Avg('rating')).get('rating__avg') or 0

    @property
    def review_count(self):
        return self.rating.count()
