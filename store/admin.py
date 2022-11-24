from django.contrib import admin

from .models import Category, Book, OrderItem, Cart, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'year', 'category', 'publisher']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['customer', 'date_ordered', 'complete', 'address', 'phone']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['book', 'cart', 'quantity']
 
@admin.register(Rating)
class RateAdmin(admin.ModelAdmin):
	list_display = ['book', 'rating', 'user']