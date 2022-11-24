from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.db.models import UniqueConstraint

from account.models import CustomUser
from .fields import IntegerRangeField


class Category(models.Model):
	title   = models.CharField(max_length=50)
	slug    = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('slug', )
		verbose_name_plural = "categories"

	def __str__(self):
		return self.title


class Book(models.Model):
	category    = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
	title       = models.CharField(max_length=200)
	slug        = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
	description = models.TextField()
	pages       = models.PositiveIntegerField()
	edition     = models.PositiveIntegerField()
	year        = models.PositiveIntegerField()
	publisher   = models.CharField(max_length=100)
	writer      = models.CharField(max_length=100)
	created     = models.DateTimeField(auto_now_add=True)
	picture     = models.ImageField(upload_to='book_pics')
	price       = models.PositiveIntegerField()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('created', )

	@property
	def rating_average(self):
		return self.rating.aggregate(models.Avg('rating')).get('rating__avg') or 0

	@property
	def review_count(self):
		return self.rating.count()


class Cart(models.Model):
	customer     = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete     = models.BooleanField(default=False)
	address      = models.TextField(null=True, blank=True)
	phone        = models.CharField(max_length=12, null=True, blank=True)

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
