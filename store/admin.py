from django.contrib import admin

from .models import (Category,
                     Book,
                     OrderItem,
                     Cart,
                     Rating,
                     Author)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_editable = ['title', ]
    list_display_links = ['slug', ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year', 'category', 'publisher']
    list_filter = ['year', 'category', 'author']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete', 'address', 'phone']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'cart', 'quantity']


@admin.register(Rating)
class RateAdmin(admin.ModelAdmin):
    list_display = ['book', 'rating', 'user']
    list_editable = ['rating']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    list_editable = ['name', ]
    list_display_links = ['slug']
