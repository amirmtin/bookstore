from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Book, Cart, OrderItem

class CategoryNav:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['catg'] = Category.objects.filter(parent=None)
		return context

class BookListView(CategoryNav, ListView):
	model = Book
	context_object_name = 'books'
	paginate_by = 3

class BookDetailView(CategoryNav, DetailView):
	model = Book 
	context_object_name = 'book'

class CartView(LoginRequiredMixin, ListView):
	template_name = 'store/cart.html'
	context_object_name = 'orders'
	
	def get_queryset(self):
		cart = Cart.objects.get(customer=self.request.user)
		orders = OrderItem.objects.filter(cart=cart)

		return orders