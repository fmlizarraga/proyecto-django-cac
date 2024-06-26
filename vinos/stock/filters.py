from django import forms
import django_filters
from django_filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Record,Branch,Product,Employee

class RecordFilter(django_filters.FilterSet):
    date = DateTimeFromToRangeFilter(
        label="Fecha (rango)",
        widget=RangeWidget(attrs={'type': 'date', 'class': 'date-range'})
    )
    typeof = django_filters.ChoiceFilter(
        choices=Record.TYPE_CHOICES,
        label="Tipo",
        widget=forms.Select(attrs={'class': 'typeof-select'})
    )
    branch = django_filters.ModelChoiceFilter(
        queryset=Branch.objects.all(), 
        label="Sucursal",
        widget=forms.Select(attrs={'class': 'branch-select'})
    )
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(), 
        label="Producto",
        widget=forms.Select(attrs={'class': 'product-select'})
    )
    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(), 
        label="Empleado",
        widget=forms.Select(attrs={'class': 'employee-select'})
    )

    class Meta:
        model = Record
        fields = ['typeof','date', 'branch', 'product', 'employee']

