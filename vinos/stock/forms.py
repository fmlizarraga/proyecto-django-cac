from typing import Any
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Product,Branch,Record,Employee,BranchStock

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

class AddRecordForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Producto")
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Empleado")

    class Meta:
        model = Record
        fields = ['product', 'quantity', 'employee', 'typeof']
        widgets = {
            'typeof': forms.HiddenInput(),
            'quantity': forms.TextInput(attrs={'class': 'input-short'})
        }
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError("La cantidad debe ser al menos una unidad.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")
        typeof = cleaned_data.get("typeof")
        employee = cleaned_data.get("employee")

        if not product or not quantity or not typeof or not employee:
            return cleaned_data

        branch = employee.branch

        branch_stock, created = BranchStock.objects.get_or_create(product=product, branch=branch)

        if typeof == Record.EXIT:
            if branch_stock.stock < quantity:
                raise ValidationError('No hay suficiente stock en la sucursal para registrar la salida.')

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

class RegisterEmployee(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="Sucursal")
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name','dni','cuil','branch']
    
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data