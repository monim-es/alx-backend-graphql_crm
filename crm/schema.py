import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter

# ======================
# GraphQL Types
# ======================
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (graphene.relay.Node,)
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node,)
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


# ======================
# Input Types
# ======================
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# ======================
# CreateCustomer
# ======================
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists.")
        try:
            validate_email(input.email)
        except ValidationError:
            raise Exception("Invalid email format.")

        customer = Customer(name=input.name, email=input.email, phone=input.phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully.")


# ======================
# BulkCreateCustomers
# ======================
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []

        for i, item in enumerate(input):
            try:
                if Customer.objects.filter(email=item.email).exists():
                    errors.append(f"Row {i+1}: Email '{item.email}' already exists.")
                    continue
                validate_email(item.email)
                customer = Customer(name=item.name, email=item.email, phone=item.phone)
                customers.append(customer)
            except ValidationError:
                errors.append(f"Row {i+1}: Invalid email format '{item.email}'.")

        created = Customer.objects.bulk_create(customers)
        return BulkCreateCustomers(customers=created, errors=errors)


# ======================
# CreateProduct
# ======================
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock):
        if Decimal(price) <= 0:
            raise Exception("Price must be positive.")
        if stock < 0:
            raise Exception("Stock cannot be negative.")
        product = Product(name=name, price=Decimal(price), stock=stock)
        product.save()
        return CreateProduct(product=product)


# ======================
# CreateOrder
# ======================
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID.")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise Exception("No valid product IDs provided.")
        if products.count() != len(product_ids):
            raise Exception("Some product IDs are invalid.")

        total_amount = sum([p.price for p in products])

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_date=order_date or timezone.now()
        )
        order.products.set(products)

        return CreateOrder(order=order)


# ======================
# Query & Mutation Root
# ======================
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    print(f"all_customers args: {all_customers.args}")
    all_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)

    # def resolve_all_customers(self, info):
    #     return Customer.objects.all()

    # def resolve_all_products(self, info):
    #     return Product.objects.all()

    # def resolve_all_orders(self, info):
    #     return Order.objects.select_related("customer").prefetch_related("products")


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
