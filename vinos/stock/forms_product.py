from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Product

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'variety', 'description', 'vintage']

        error_messages = {
            'name': {
                'required': 'El nombre es obligatorio'
            },
            'variety': {
                'required': 'El varietal es obligatorio'
            },
            'vintage': {
                'required': 'La cosecha es obligatoria'
            },
        }
    
    def clean_vintage(self):
        vintage = self.cleaned_data.get('vintage')
        current_year = datetime.now().year
        if vintage < 1900 or vintage > current_year:
            raise ValidationError("Por favor ingrese un año válido.")
        return vintage

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        variety = cleaned_data.get('variety')

        if name and variety and name == variety:
            raise ValidationError("El nombre y el varietal no pueden ser iguales.")

        return cleaned_data
    
    def save(self, commit=True):
        product = super(AddProductForm, self).save(commit=False)
        if commit:
            product.save()
            self.save_m2m()
        return product

class SelectProductForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),  # No cargamos productos aquí
        label="Producto",
        widget=forms.Select(attrs={'class': 'product-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['product'].queryset = Product.objects.filter(id=product_id)
            except (ValueError, TypeError):
                pass  # en caso de que el ID no sea válido

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError("Seleccione un producto válido.")
        return product
