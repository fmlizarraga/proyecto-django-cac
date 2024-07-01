from django import forms
from django.core.exceptions import ValidationError
from .models import Product,Record,BranchStock

class AddRecordForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={'class': 'product-select'})
    )

    MIN_QUANTITY = 1
    ERROR_QUANTITY_MSG = "La cantidad debe ser al menos una unidad."
    ERROR_STOCK_MSG = "No hay suficiente stock en la sucursal para registrar la salida."

    class Meta:
        model = Record
        fields = ['product', 'quantity', 'typeof']
        widgets = {
            'typeof': forms.HiddenInput(),
            'quantity': forms.TextInput(attrs={'class': 'input-short'}),
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['product'].queryset = Product.objects.filter(id=product_id)
            except (ValueError, TypeError):
                pass  # en caso de que el ID no sea válido
        """Mantener el producto seleccionado disponible en el queryset"""
        if self.instance and self.instance.pk:
            self.fields['product'].queryset = Product.objects.filter(pk=self.instance.product.pk) | Product.objects.all()

    def clean_quantity(self):
        """Valida que la cantidad sea mayor o igual a la mínima permitida."""
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < self.MIN_QUANTITY:
            raise ValidationError(self.ERROR_QUANTITY_MSG)
        return quantity
    
    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError("Seleccione un producto válido.")
        return product

    def clean(self):
        """Realiza validaciones adicionales y asegura que el stock sea suficiente para registrar la salida."""
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")
        typeof = cleaned_data.get("typeof")

        if not all([product, quantity, typeof]):
            return cleaned_data

        branch = self.employee.branch

        """Intentar obtener el stock de la sucursal"""
        branch_stock = BranchStock.objects.filter(product=product, branch=branch).first()

        if self.instance and self.instance.pk:
            # Caso de edición
            original_record = Record.objects.get(pk=self.instance.pk)
            original_quantity = original_record.quantity

            # Si se está cambiando de producto o si la cantidad ha cambiado
            if (product != original_record.product or quantity != original_quantity) and typeof == Record.EXIT:
                if branch_stock and branch_stock.stock + original_quantity < quantity:
                    raise ValidationError(self.ERROR_STOCK_MSG)
        else:
            # Caso de creación
            if typeof == Record.EXIT and branch_stock and branch_stock.stock < quantity:
                raise ValidationError(self.ERROR_STOCK_MSG)

        return cleaned_data

    def save(self, commit=True):
        """Guarda el registro con el empleado asociado."""
        record = super().save(commit=False)
        record.employee = self.employee
        if commit:
            record.save()
        return record
