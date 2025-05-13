import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .shop_models import Product

@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for testing purposes
class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        product_data = [
            {
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "created_date": product.created_date.isoformat()
            }
            for product in products
        ]
        return JsonResponse(product_data, safe=False)

    def post(self, request):
        try:
            # Try to parse JSON request body
            data = json.loads(request.body.decode("utf-8"))
            name = data.get("name")
            description = data.get("description")
            price = data.get("price")
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        if name and description and price is not None:
            try:
                new_product = Product.objects.create(name=name, description=description, price=price)
                product_data = {
                    "name": new_product.name,
                    "description": new_product.description,
                    "price": str(new_product.price),
                    "created_date": new_product.created_date.isoformat()
                }
                return JsonResponse(product_data, status=201)
            except ValueError:
                return JsonResponse({"error": "Invalid price format."}, status=400)

        return JsonResponse({"error": "Name, description, and price are required."}, status=400)