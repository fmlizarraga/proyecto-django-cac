from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Product,Branch

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

class RegisterBranch(forms.ModelForm):
    area_code = forms.CharField(
        max_length=5, 
        label="Código de Área",
        widget=forms.TextInput(attrs={'class': 'telephone-pre'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        label="Número de Teléfono",
        widget=forms.TextInput(attrs={'class': 'telephone-sub'})
    )

    class Meta:
        model = Branch
        fields = ['name', 'address', 'telephone']
        widgets = {
            'telephone': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telephone'].required = False

    def clean(self):
        cleaned_data = super().clean()
        area_code = cleaned_data.get("area_code")
        phone_number = cleaned_data.get("phone_number")

        full_phone_number = f"+54{area_code}{phone_number}"
        
        phone_validator = RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono no válido.')
        try:
            phone_validator(full_phone_number)
        except ValidationError as e:
            self.add_error('phone_number', e)
        
        cleaned_data['telephone'] = full_phone_number

        return cleaned_data
