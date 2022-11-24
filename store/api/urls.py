from django.urls import path

from . import api

app_name = 'api'

urlpatterns = [
	path(
		route='cart/',
		view=api.CartApiView.as_view(),
		name='add_to_cart'
	),
	path(
		route='rate/',
		view=api.RateApiView.as_view(),
		name='rating'
		),
]