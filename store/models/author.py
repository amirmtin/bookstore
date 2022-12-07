from django.db import models
from django_extensions.db.fields import AutoSlugField


class Author(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, editable=False)
    about = models.TextField()

    def __str__(self):
        return self.name
