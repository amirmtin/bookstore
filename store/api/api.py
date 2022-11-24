from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from store.models import Cart, Book, OrderItem, Rating
from .permissions import IsVerified


class CartApiView(APIView):
    permission_classes = [IsVerified, IsAuthenticated, ]
    
    def post(self, request):
        data = request.data
        cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
        book = Book.objects.get(slug=data['book'])
        order_item, created = OrderItem.objects.get_or_create(cart=cart, book=book)
        order_item.quantity = order_item.quantity + 1
        order_item.save()
        return Response({'message': 'done'}, status=status.HTTP_200_OK)
    
    def put(self, request):
        data = request.data
        print(data)
        action = data['action']
        cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
        book = Book.objects.get(slug=data['book'])
        order_item, created = OrderItem.objects.get_or_create(cart=cart, book=book)
        
        order_item.quantity = order_item.quantity + action
        if order_item.quantity == 0:
            order_item.delete()
        else:
            order_item.save()
            
        return Response({'message': 'done'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        data = request.data
        cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
        book = Book.objects.get(slug=data['book'])
        order_item, created = OrderItem.objects.get_or_create(cart=cart, book=book)
        order_item.delete()
        
        return Response({'message': 'done'}, status=status.HTTP_200_OK)

    
class RateApiView(APIView):
    permission_classes = [IsVerified, IsAuthenticated, ]
    
    def get(self, request):
        slug = request.GET.get('book')
        
        try:
            book = Book.objects.get(slug=slug) 
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        try:
            rate = Rating.objects.get(book=book, user=request.user)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(
            {
                'rate': rate.rating
            }
        )

    def post(self, request):
        data = request.data
        rate = data['rating']
        
        if rate > 5 or rate < 1:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = Book.objects.get(slug=data['book']) 
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        new_rate, created = Rating.objects.get_or_create(user=request.user, book=book)
        new_rate.rating = rate
        new_rate.save()
        return Response({'message': 'done'}, status=status.HTTP_200_OK)
