from django import forms
from django.contrib.auth.models import Group
from .models import Branch,Employee

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
