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
        product.quantity = 0  # Ensure quantity is set to 0
        if commit:
            product.save()
            self.save_m2m()  # To save ManyToMany field if necessary
        return product

class AddRecordForm(forms.Form):
    prid = forms.IntegerField(
        label="Código",
        required=True
    )
    quantity = forms.IntegerField(
        label="Cantidad",
        required=True
    )
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError("La cantidad debe ser al menos una unidad.")
        return quantity
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data