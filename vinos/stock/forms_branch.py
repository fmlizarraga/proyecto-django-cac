from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Branch

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

        if self.instance and self.instance.pk:
            telephone = self.instance.telephone
            if telephone:
                # Suponiendo que el formato del telefono es "+54<area_code><phone_number>"
                area_code = telephone[3:5]  # Extraer la parte del codigo de area
                phone_number = telephone[5:]  # Extraer la parte del numero de telefono

                self.fields['area_code'].initial = area_code
                self.fields['phone_number'].initial = phone_number

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

class SelectBranchForm(forms.Form):
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        label="Sucursal"
    )
