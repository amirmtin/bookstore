from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from store.models import Cart, Book, OrderItem

@api_view(['POST'])
def add_to_cart(request):
	if not request.user.is_authenticated:
		return Response({'message': 'login required'}, status=status.HTTP_401_UNAUTHORIZED)

	elif not request.user.is_verified:
		return Response({'message': 'email not verified'}, status=status.HTTP_403_FORBIDDEN)
	
	else:
		data = request.data
		cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
		book = Book.objects.get(slug=data['book'])
		order_item, created = OrderItem.objects.get_or_create(cart=cart, book=book)
		order_item.quantity = order_item.quantity + 1
		order_item.save()

		return Response({'message': 'done'}, status=status.HTTP_200_OK)