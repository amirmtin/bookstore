from django.urls import path

from . import api

app_name = 'api'

urlpatterns = [
	path(
		route='cart',
		view=api.add_to_cart,
		name='add_to_cart'
	),
]