from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class AddProductForm(forms.Form):
    name = forms.CharField(
        label="Nombre", 
        required=True
    )
    vintage = forms.IntegerField(
        label="Cosecha",
        required=True
    )
    variety = forms.CharField(
        label="Varietal", 
        required=True
    )
    description = forms.CharField(
        label="Descripción",
        required=True,
        widget=forms.Textarea(attrs={'class': 'input-desc'})
    )
    quantity = forms.IntegerField(
        label="Cantidad",
        required=True
    )
    def clean_vintage(self):
        vintage = self.cleaned_data.get('vintage')
        current_year = datetime.now().year
        if vintage < 1900 or vintage > current_year:
            raise ValidationError("Por favor ingrese un año válido.")
        return vintage

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        variety = cleaned_data.get('variety')

        if name and variety and name == variety:
            raise ValidationError("El nombre y el varietal no pueden ser iguales.")

        return cleaned_data

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