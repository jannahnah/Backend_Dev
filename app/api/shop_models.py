# shop/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.URLField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()  # Assuming a simple integer for user identification

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Checkout(models.Model):
    checkout_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50)  # e.g., 'Pending', 'Completed'
    created_at = models.DateTimeField(auto_now_add=True)

class CheckoutItem(models.Model):
    checkout_item_id = models.AutoField(primary_key=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='checkout_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)