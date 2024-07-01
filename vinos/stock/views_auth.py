from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from .decorators import anonymous_required
from .forms import LoginUser,RegisterUser

@anonymous_required
def register_user(req):
    if req.method == 'POST':
        form = RegisterUser(req.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(req, f'Cuenta creada para {username}!')
            login(req,user)
            return redirect('index')
    else:
        form = RegisterUser()
    return render(req, 'forms/register.html', {'form': form})

@anonymous_required
def login_user(req):
    if req.method == 'POST':
        form = LoginUser(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, f'Bienvenid@, {username}!')
                return redirect('index')
            else:
                messages.error(req, 'Usuario o contraseña inválido')
    else:
        form = LoginUser()
    return render(req, 'forms/login.html', {'form': form})

def logout_user(req):
    logout(req)
    messages.success(req, 'Has sido desconectado.')
    return redirect('login')

def inactive_user(req):
    context = {
        'title': 'Usuario inactivo',
        'message': 'Tu cuenta está inactiva. Contacta con el administrador.'
    }
    return render(req, 'pages/inactive_user.html', context)