from django.db import models
from django.core.exceptions import ValidationError
from django_extensions.db.fields import AutoSlugField

from account.models import CustomUser

class Category(models.Model):
	parent  = models.ForeignKey('self', 
				related_name='children', 
				on_delete=models.CASCADE, 
				null=True, 
				blank=True)
	title   = models.CharField(max_length=50)
	slug    = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('slug', 'parent',)
		verbose_name_plural = "categories"

	def __str__(self):
		return self.title

	def get_parents(self):
		count = 1  
		parent = self.parent

		if not parent:
			return count

		while 1:
			parent = parent.parent
			print(parent)
			if parent:
				count += 1
			else:
				break

		return count

	def clean(self):
		super(Category, self).clean()

		parents = self.get_parents()
		if parents > 2:
			raise ValidationError('Each category can have a maximum of 2 parents')

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
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.book} {self.quantity}'

	@property
	def get_total(self):
		total = self.book.price * self.quantity
		return total