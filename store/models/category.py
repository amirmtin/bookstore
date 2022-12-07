from django.db import models
from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('slug',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
