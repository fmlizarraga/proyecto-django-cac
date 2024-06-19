from django.contrib import admin
from .models import Product, Branch, Record, Employee, BranchStock

admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(Record)
admin.site.register(Employee)
admin.site.register(BranchStock)