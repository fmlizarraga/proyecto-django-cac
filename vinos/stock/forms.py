from typing import Any
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

class SelectProductForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Producto",
        widget=forms.Select(attrs={'class': 'select2'})
    )

class AddRecordForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(), 
        label="Producto",
        widget=forms.Select(attrs={'class': 'select2'})
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

    def clean_quantity(self):
        """Valida que la cantidad sea mayor o igual a la mínima permitida."""
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < self.MIN_QUANTITY:
            raise ValidationError(self.ERROR_QUANTITY_MSG)
        return quantity

    def clean(self):
        """Realiza validaciones adicionales y asegura que el stock sea suficiente para registrar la salida."""
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")
        typeof = cleaned_data.get("typeof")

        if not all([product, quantity, typeof]):
            return cleaned_data

        branch = self.employee.branch

        # Intentar obtener o crear el stock de la sucursal
        branch_stock, created = BranchStock.objects.get_or_create(product=product, branch=branch)

        if typeof == Record.EXIT and branch_stock.stock < quantity:
            raise ValidationError(self.ERROR_STOCK_MSG)

        return cleaned_data

    def save(self, commit=True):
        """Guarda el registro con el empleado asociado."""
        record = super().save(commit=False)
        record.employee = self.employee
        if commit:
            record.save()
        return record

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

class RegisterUser(UserCreationForm):
    username = forms.CharField(max_length=100, label="Nombre de usuario", required=True, help_text="Requerido. 100 caracteres o menos. Solo letras, numeros y @/./+/-/_.")
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de email válida.")
    first_name = forms.CharField(max_length=100, label="Nombre(s)")
    last_name = forms.CharField(max_length=100,label="Apellido(s)")
    dni = forms.IntegerField(label="DNI")
    cuil = forms.CharField(max_length=13, label="CUIL", help_text="Formato: NN-NNNNNNNN-N")
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="Sucursal")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

            group, created = Group.objects.get_or_create(name='Workers')
            user.groups.add(group)
            
            Employee.objects.create(
                user=user,
                dni=self.cleaned_data['dni'],
                cuil=self.cleaned_data['cuil'],
                branch=self.cleaned_data['branch']
            )
        return user

class EditEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Nombre(s)")
    last_name = forms.CharField(max_length=100, label="Apellido(s)")
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de email válida.")
    dni = forms.IntegerField(label="DNI")
    cuil = forms.CharField(max_length=13, label="CUIL", help_text="Formato: NN-NNNNNNNN-N")
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="Sucursal", help_text="Transferir empleado a otra sucursal.")
    is_active = forms.BooleanField(required=False, label="Empleado activo", help_text="Desactivar para suspender al empleado.")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grupo", help_text="Seleccione el grupo del empleado.")

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'dni', 'cuil', 'branch', 'is_active', 'group']

    def __init__(self, *args, **kwargs):
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields['group'].initial = self.instance.user.groups.first()

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Update the user's group
        group = self.cleaned_data['group']
        user.groups.clear()
        user.groups.add(group)

        if commit:
            user.save()
            employee.save()
        return employee

class LoginUser(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)