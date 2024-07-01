from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Branch,Employee

class LoginUser(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

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
