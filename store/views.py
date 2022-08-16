from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Category, Book, Cart, OrderItem
from .forms import CheckOutForm

class CategoryNav:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.filter(parent=None)
		return context

class BookListView(CategoryNav, ListView):
	model = Book
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		books    = super().get_queryset()
		category = self.request.GET.get('cat')

		if category:
			books = books.filter(category__slug=category)

		query = self.request.GET.get('q')

		if query:
			books = books.filter(
					Q(title__icontains=query) |
					Q(description__icontains=query) |
					Q(publisher__icontains=query) |
					Q(writer__icontains=query)
				)

		return books

class BookDetailView(CategoryNav, DetailView):
	model = Book 
	context_object_name = 'book'

class CartView(LoginRequiredMixin, ListView):
	template_name = 'store/cart.html'
	context_object_name = 'orders'
	
	def get_queryset(self):
		cart, created = Cart.objects.get_or_create(customer=self.request.user, complete=False)
		orders = OrderItem.objects.filter(cart=cart)

		return orders

class CheckOutView(LoginRequiredMixin, FormView):
	template_name = 'store/checkout.html'
	form_class = CheckOutForm 

	def get(self, *args, **kwargs):
		user = self.request.user 

		if not user.is_verified:
			return redirect('account:send_email')

		try:
			cart = Cart.objects.get(customer=user, complete=False)
		except Cart.DoesNotExist:
			return redirect('store:list')

		orders = OrderItem.objects.filter(cart=cart)

		if not orders.count():
			return redirect('store:list')

		return super(CheckOutView, self).get(self, self.request)

	def post(self, *args, **kwargs):
		user = self.request.user 

		if not user.is_verified:
			return redirect('account:send_email')

		try:
			cart = Cart.objects.get(customer=user, complete=False)
		except Cart.DoesNotExist:
			return redirect('store:list')


		orders = OrderItem.objects.filter(cart=cart)
		
		if not orders.count():
			return redirect('store:list')

		form = CheckOutForm(self.request.POST) 

		if form.is_valid():
			address = form.cleaned_data.get('address')
			phone   = form.cleaned_data.get('phone')

			cart.address = address
			cart.phone   = phone
			cart.complete = True 
			cart.save()

			return render(self.request, 'store/order_complete.html')
		else:
			return render(self.request, 'store/checkout.html', {'form': form})
