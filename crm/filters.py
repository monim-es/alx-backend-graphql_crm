import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    order_by = django_filters.OrderingFilter(fields=[
        ('name', 'name'),
        ('email', 'email'),
    ])

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = []

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stock__gte = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stock__lte = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")

    order_by = django_filters.OrderingFilter(fields=[
        ('name', 'name'),
        ('price', 'price'),
        ('stock', 'stock'),
    ])

    class Meta:
        model = Product
        fields = []

class OrderFilter(django_filters.FilterSet):
    total_amount__gte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    total_amount__lte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")
    order_date__gte = django_filters.DateTimeFilter(field_name="order_date", lookup_expr="gte")
    order_date__lte = django_filters.DateTimeFilter(field_name="order_date", lookup_expr="lte")
    customer_name = django_filters.CharFilter(method='filter_customer_name')
    product_name = django_filters.CharFilter(method='filter_product_name')
    product_id = django_filters.NumberFilter(field_name="products__id")

    order_by = django_filters.OrderingFilter(fields=[
        ('total_amount', 'total_amount'),
        ('order_date', 'order_date'),
    ])

    def filter_customer_name(self, queryset, name, value):
        return queryset.filter(customer__name__icontains=value)

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(products__name__icontains=value)

    class Meta:
        model = Order
        fields = []
