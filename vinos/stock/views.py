from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Product,Branch,Record,BranchStock,Employee
from .forms import AddProductForm,AddRecordForm,RegisterBranch,LoginUser,RegisterUser

def anonymous_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def index(req):
    context = {
        'title': 'Control de stock'
    }

    return render(req, 'pages/index.html', context)

class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-vintage','name']
    template_name = 'pages/product_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vinos disponibles'

        return context

def product_detail(req, pid):
    product = get_object_or_404(Product,pk=pid)

    context = {
        'title': 'Detalle de producto',
        'product': product
    }

    return render(req, 'pages/product_detail.html', context)

@login_required
def add_product(req):
    context = {
        'title': 'Nuevo Producto',
    }

    if req.method == 'POST':
        form = AddProductForm(req.POST)

        if form.is_valid():
            product = form.save()
            messages.success(req, '¡El producto fue agregado al inventario con exito!')
            return redirect('product_list')
    else:
        form = AddProductForm()
    
    context['form'] = form
    return render(req, 'forms/add_product.html', context)

@login_required
def add_record(req, type):
    TYPE_CHOICES = {
        'entry': Record.ENTRY,
        'exit': Record.EXIT,
    }

    if type not in TYPE_CHOICES:
        messages.error(req, 'Tipo de registro no válido.')
        return redirect('index')
    
    try:
        employee = Employee.objects.get(user=req.user)
    except Employee.DoesNotExist:
        return redirect('index')  # Redirigir a una página de error si el empleado no existe
    
    context = {}
    if type == Record.ENTRY:
        context['title'] = "Ingreso"
    elif type == Record.EXIT:
        context['title'] = "Egreso"
    
    if req.method == 'POST':
        form = AddRecordForm(req.POST, employee=employee)

        if form.is_valid():
            record = form.save(commit=False)
            record.typeof = TYPE_CHOICES[type]
            employee = record.employee
            branch = employee.branch
            record.branch = branch

            branch_stock, created = BranchStock.objects.get_or_create(
                product=record.product, 
                branch=branch
            )


            if record.typeof == Record.ENTRY:
                branch_stock.stock += record.quantity
            elif record.typeof == Record.EXIT:
                if branch_stock.stock < record.quantity:
                    messages.error(req, 'No hay suficiente stock en la sucursal para registrar la salida.')
                    return render(req, 'forms/add_record.html', context)

                branch_stock.stock -= record.quantity

            branch_stock.save()
            record.save()

            messages.success(req, '¡El registro se creó con éxito y el stock se actualizó!')
            return redirect('record_list')
        else:
            messages.error(req, 'Error al crear el registro. Verifique los datos ingresados.')
    else:
        form = AddRecordForm(initial={'typeof': TYPE_CHOICES[type]}, employee=employee)

    context['form'] = form
    return render(req, 'forms/add_record.html', context)

@login_required
def product_autocomplete(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(name__icontains=q)
        results = [{'id': product.pk, 'text': product.name} for product in products]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

class BaseRecordsListView(LoginRequiredMixin, ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'pages/record_list.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            return redirect('index')  # Redirigir

        context['employee'] = employee

        return context

class RecordsByBranch(BaseRecordsListView):
    ordering = ['branch']
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registros (Sucursal)'
        context['order'] = 'branch'
        return context

class RecordsByTime(BaseRecordsListView):
    ordering = ['date']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registros (Hora)'
        context['order'] = 'time'
        return context

@login_required
def register_branch(req):
    context = {
        'title': 'Registrar Sucursal'
    }

    if req.method == 'POST':
        form = RegisterBranch(req.POST)

        if form.is_valid():
            form.save()
            messages.success(req, '¡La sucursal se registró con exito!')
            return redirect('branch_list')
    else:
        form = RegisterBranch()
    
    context['form'] = form

    return render(req, 'forms/register_branch.html', context)

@login_required
def branch_list(req):
    branches = Branch.objects.all()
    context = {
        'title': 'Sucursales',
        'branches': branches
    }

    return render(req, 'pages/branch_list.html', context)

@login_required
def employee_list(req):
    employees = Employee.objects.all()
    context = {
        'title': 'Empleados',
        'employees': employees
    }

    return render(req, 'pages/employee_list.html', context)

@login_required
def branch_stock_list(req):
    employee = Employee.objects.get(user=req.user)
    branch = employee.branch
    stock = BranchStock.objects.filter(branch=branch)
    context = {
        'title': 'Stock en la sucursal',
        'stock': stock,
        'branch': branch
    }

    return render(req, 'pages/stock_list.html', context)

@login_required
@permission_required('stock.change_employee', raise_exception=False)
def administrate(req):
    context = {
        'title': 'Administrar'
    }

    return render(req, 'pages/admin_page.html', context)

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