import django_filters
from django_filters import DateTimeFromToRangeFilter
from .models import Record,Branch,Product,Employee

class RecordFilter(django_filters.FilterSet):
    date = DateTimeFromToRangeFilter(label="Fecha (rango)")
    branch = django_filters.ModelChoiceFilter(queryset=Branch.objects.all(), label="Sucursal")
    product = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), label="Producto")
    employee = django_filters.ModelChoiceFilter(queryset=Employee.objects.all(), label="Empleado")
    typeof = django_filters.ChoiceFilter(choices=Record.TYPE_CHOICES, label="Tipo")

    class Meta:
        model = Record
        fields = ['date', 'branch', 'product', 'employee', 'typeof']
