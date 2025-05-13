import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .shop_models import Product, Cart, CartItem, Checkout, CheckoutItem, Category  # Added Category import

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, request):
        products = Product.objects.select_related('category').values(
            'product_id', 'name', 'price', 'description', 'stock', 'image_url', 'category__name'
        )
        return JsonResponse(list(products), safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            
            required_fields = ['name', 'price', 'description', 'stock', 'image_url', 'category_id']
            if not all(field in data for field in required_fields):
                missing = [field for field in required_fields if field not in data]
                return JsonResponse({'error': f'Missing required fields: {missing}'}, status=400)
            
            try:
                category = Category.objects.get(pk=data['category_id'])
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=400)
            
            # Validate stock is positive
            if int(data['stock']) < 0:
                return JsonResponse({'error': 'Stock cannot be negative'}, status=400)
            
            product = Product.objects.create(
                name=data['name'],
                price=data['price'],
                description=data['description'],
                stock=data['stock'],
                image_url=data['image_url'],
                category=category
            )
            
            return JsonResponse({
                'message': 'Product created successfully',
                'product_id': product.product_id,
                'name': product.name,
                'price': str(product.price),
                'stock': product.stock,
                'category': product.category.name
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            if not all([user_id, product_id]):
                return JsonResponse({'error': 'Missing user_id or product_id'}, status=400)
            
            if quantity <= 0:
                return JsonResponse({'error': 'Quantity must be positive'}, status=400)
            
            cart, _ = Cart.objects.get_or_create(user_id=user_id)
            product = Product.objects.get(product_id=product_id)
            
            if product.stock < quantity:
                return JsonResponse({'error': 'Insufficient stock'}, status=400)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({'message': 'Product added to cart'}, status=201)
            
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'user_id is required'}, status=400)
                
            cart = Cart.objects.filter(user_id=user_id).first()
            if not cart:
                return JsonResponse({'message': 'Cart not found'}, status=404)

            items = list(cart.items.select_related('product').values(
                'product__product_id',
                'product__name',
                'product__price',
                'quantity'
            ))
            return JsonResponse(items, safe=False)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if not user_id:
                return JsonResponse({'error': 'user_id is required'}, status=400)
                
            cart = Cart.objects.filter(user_id=user_id).first()
            if not cart or not cart.items.exists():
                return JsonResponse({'message': 'Cart is empty or not found'}, status=404)

            total_amount = 0
            checkout_items = []
            
            # Verify stock before checkout
            for item in cart.items.select_related('product').all():
                if item.quantity > item.product.stock:
                    return JsonResponse(
                        {'error': f'Insufficient stock for {item.product.name}'},
                        status=400
                    )
            
            # Process checkout
            for item in cart.items.select_related('product').all():
                subtotal = item.product.price * item.quantity
                total_amount += subtotal
                
                # Reduce product stock
                item.product.stock -= item.quantity
                item.product.save()
                
                checkout_items.append({
                    'product_id': item.product.product_id,
                    'quantity': item.quantity,
                    'subtotal': subtotal
                })

            checkout = Checkout.objects.create(
                user_id=user_id,
                total_amount=total_amount,
                payment_status='Pending'
            )

            for item in checkout_items:
                CheckoutItem.objects.create(
                    checkout=checkout,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    subtotal=item['subtotal']
                )
            
            # Clear the cart after successful checkout
            cart.items.all().delete()
            
            return JsonResponse({
                'message': 'Checkout successful',
                'checkout_id': checkout.checkout_id,
                'total_amount': str(total_amount),
                'items': checkout_items
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = list(Category.objects.values('id', 'name'))
        return JsonResponse(categories, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'name' not in data or not data['name'].strip():
                return JsonResponse({'error': 'Category name is required'}, status=400)
            
            if Category.objects.filter(name=data['name'].strip()).exists():
                return JsonResponse({'error': 'Category already exists'}, status=400)
            
            category = Category.objects.create(name=data['name'].strip())
            return JsonResponse({
                'message': 'Category created',
                'id': category.id,
                'name': category.name
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)