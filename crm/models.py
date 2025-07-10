from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    
class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)