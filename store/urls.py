from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
	path(
		route='',
		view=views.BookListView.as_view(),
		name='list'
		),
	path(
		route='detail/<slug:slug>/',
		view=views.BookDetailView.as_view(),
		name='detail'
		),
	path(
		route='cart/',
		view=views.CartView.as_view(),
		name='cart'
		),
	path(
		route='checkout/',
		view=views.CheckOutView.as_view(),
		name='checkout'
		),
	path(
		route='callback-gateway/', 
		view=views.callback_gateway_view, 
		name='callback-gateway'
		),
]