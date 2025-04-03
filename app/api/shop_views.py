from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Checkout
from .serializers import ProductSerializer, CartSerializer, CheckoutSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = Cart.objects.get(user_id=request.user.id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        cart = Cart.objects.get(user_id=request.user.id)
        product = Product.objects.get(id=request.data['product_id'])
        quantity = request.data['quantity']
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        return Response({'message': 'Product added to cart'})

class CheckoutViewSet(viewsets.ViewSet):
    def create(self, request):
        cart = Cart.objects.get(user_id=request.user.id)
        total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        checkout = Checkout.objects.create(cart=cart, total_price=total_price)
        return Response({'message': 'Checkout successful', 'total_price': total_price})