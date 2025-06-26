# seed_db.py

import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order
from django.utils import timezone

# Clear previous data (optional)
Order.objects.all().delete()
Customer.objects.all().delete()
Product.objects.all().delete()

# Seed Customers
customers = []
for i in range(5):
    c = Customer.objects.create(
        name=f"Customer {i+1}",
        email=f"customer{i+1}@example.com",
        phone=f"+123456789{i}"
    )
    customers.append(c)

# Seed Products
products = []
for i in range(5):
    p = Product.objects.create(
        name=f"Product {i+1}",
        price=Decimal(random.randint(10, 100)),
        stock=random.randint(5, 20)
    )
    products.append(p)

# Seed Orders
for i in range(3):
    customer = random.choice(customers)
    selected_products = random.sample(products, k=2)
    total_amount = sum(p.price for p in selected_products)

    order = Order.objects.create(
        customer=customer,
        total_amount=total_amount,
        order_date=timezone.now()
    )
    order.products.set(selected_products)

print("✅ Database seeded with test customers, products, and orders.")
