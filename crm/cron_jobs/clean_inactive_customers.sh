#!/bin/bash

cd "/mnt/c/Users/lenovo/Desktop/alx django/alx-backend-graphql_crm"

timestamp=$(date "+%Y-%m-%d %H:%M:%S")

deleted_count=$("/mnt/c/Users/lenovo/Desktop/alx django/venv_alxtravel/Scripts/python.exe" manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

cutoff_date = timezone.now() - timedelta(days=365)
qs = Customer.objects.annotate(order_count=Count('orders')).filter(order_count=0, created_at__lt=cutoff_date)
count = qs.count()
for customer in qs:
    customer.delete()
print('DELETED:' + str(count))
" | grep 'DELETED:' | cut -d':' -f2)

echo "$timestamp - Deleted $deleted_count inactive customers" >> crm/cron_jobs/customer_cleanup_log.txt
