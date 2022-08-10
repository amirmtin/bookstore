from django.contrib import admin

from .models import Category, Book, OrderItem, Cart

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'parent', 'slug']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'year', 'category', 'publisher']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['customer', 'date_ordered', 'complete', 'address', 'phone']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['book', 'cart', 'quantity']