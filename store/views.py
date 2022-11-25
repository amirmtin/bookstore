from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import Http404
from django.contrib import messages
from django.db.models import Avg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Category, Book, Cart, OrderItem
from .forms import CheckOutForm


class CategoryNav:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context


class BookListView(CategoryNav, ListView):
	model = Book
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		books = super().get_queryset().annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')
		category = self.request.GET.get('cat')

		if category:
			books = books.filter(category__slug=category)

		query = self.request.GET.get('q')

		if query:
			vector = SearchVector('title', 'description', 'publisher', 'writer')
			query = SearchQuery(query)
			books.annotate(rank=SearchRank(vector, query)).order_by('-rank')

		return books


class BookDetailView(CategoryNav, DetailView):
	model = Book 
	context_object_name = 'book'


class CartView(LoginRequiredMixin, ListView):
	template_name = 'store/cart.html'
	context_object_name = 'orders'
	
	def get_queryset(self):
		cart, created = Cart.objects.get_or_create(customer=self.request.user, complete=False)
		orders = OrderItem.objects.filter(cart=cart).select_related('book')

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
			cart.save()

			amount = cart.get_cart_total
			user_mobile_number = phone

			factory = bankfactories.BankFactory()

			try:
				bank = factory.create()
				bank.set_request(self.request)
				bank.set_amount(amount)
				bank.set_client_callback_url(reverse('store:callback-gateway'))
				bank.set_mobile_number(user_mobile_number)
				bank_record = bank.ready()
				return bank.redirect_gateway()
			except AZBankGatewaysException as e:
				raise e

		else:
			return render(self.request, 'store/checkout.html', {'form': form})


def callback_gateway_view(request):
	tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
	if not tracking_code:
		raise Http404

	try:
		bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
	except bank_models.Bank.DoesNotExist:
		raise Http404

	if bank_record.is_success:
		user = request.user
		try:
			cart = Cart.objects.get(customer=user, complete=False)
		except Cart.DoesNotExist:
			return redirect('store:list')

		orders = OrderItem.objects.filter(cart=cart)

		if not orders.count():
			return redirect('store:list')

		cart.complete = True
		cart.save()
		return render(request, 'store/order_complete.html')

	messages.add_message(request, messages.INFO, 'payment was not successfull')
	return redirect('store:list')
