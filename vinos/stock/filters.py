from django import forms
import django_filters
from django_filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Record,Branch,Product,Employee

class RecordFilter(django_filters.FilterSet):
    RECORD_CHOICES = [
        (Record.ENTRY, 'Entrada'),
        (Record.EXIT, 'Salida')
    ]
    date = DateTimeFromToRangeFilter(
        label="Fecha (rango)",
        widget=RangeWidget(attrs={'type': 'date', 'class': 'date-range'})
    )
    typeof = django_filters.ChoiceFilter(
        choices=RECORD_CHOICES,
        label="Tipo",
        widget=forms.Select(attrs={'class': 'typeof-select'})
    )
    branch = django_filters.ModelChoiceFilter(
        queryset=Branch.objects.all(), 
        label="Sucursal",
        widget=forms.Select(attrs={'class': 'branch-select'})
    )
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={'class': 'product-select'})
    )
    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.none(),
        label="Empleado",
        widget=forms.Select(attrs={'class': 'employee-select'})
    )

    class Meta:
        model = Record
        fields = ['typeof','date', 'branch', 'product', 'employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.filters['product'].queryset = Product.objects.filter(id=product_id)
            except (ValueError, TypeError):
                pass

        if 'employee' in self.data:
            try:
                employee_id = int(self.data.get('employee'))
                self.filters['employee'].queryset = Employee.objects.filter(id=employee_id)
            except (ValueError, TypeError):
                pass