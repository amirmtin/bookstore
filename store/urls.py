from django.urls import path 

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
]