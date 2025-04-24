# shop/views.py
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..shop.models import Product, Cart, CartItem, Checkout, CheckoutItem

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, request):
        products = list(Product.objects.values())
        return JsonResponse(products, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CartView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Get or create a cart for the user
        cart, created = Cart.objects.get_or_create(user_id=user_id)

        # Add product to cart
        product = Product.objects.get(product_id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({'message': 'Product added to cart'}, status=201)

    def get(self, request):
        user_id = request.GET.get('user_id')
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            return JsonResponse({'message': 'Cart not found'}, status=404)

        items = list(cart.items.values('product__name', 'product__price', 'quantity'))
        return JsonResponse(items, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get('user_id')
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            return JsonResponse({'message': 'Cart not found'}, status=404)

        total_amount = 0
        checkout_items = []

        for item in cart.items.all():
            subtotal = item.product.price * item.quantity
            total_amount += subtotal
            checkout_items.append({
                'product_id': item.product.product_id,
                'quantity': item.quantity,
                'subtotal': subtotal
            })

        checkout = Checkout.objects.create(user_id=user_id, total_amount=total_amount, payment_status='Pending')

        for checkout_item in checkout_items:
            CheckoutItem.objects.create(
                checkout=checkout,
                product_id=checkout_item['product_id'],
                quantity=checkout_item['quantity'],
                subtotal=checkout_item['subtotal']
            )

        return JsonResponse({'message': 'Checkout successful', 'total_amount': total_amount}, status=201)