from typing import Any
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView, UpdateView
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django_filters.views import FilterView
from .models import Product,Branch,Record,BranchStock,Employee
from .forms import AddProductForm,AddRecordForm,RegisterBranch,LoginUser,RegisterUser,SelectProductForm,EditEmployeeForm,SelectBranchForm
from .decorators import active_employee_required,anonymous_required,ActiveEmployeeRequiredMixin
from .filters import RecordFilter

def index(req):
    context = {
        'title': 'Control de stock'
    }

    return render(req, 'pages/index.html', context)

class ProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-vintage','name']
    template_name = 'pages/product_list.html'
    permission_required = 'stock.view_product'
    raise_exception = True

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vinos disponibles'

        return context

@login_required
@active_employee_required
@permission_required('stock.view_product',raise_exception=True)
def product_detail(req, pid):
    product = get_object_or_404(Product,pk=pid)

    context = {
        'title': 'Detalle de producto',
        'product': product
    }

    return render(req, 'pages/product_detail.html', context)

@active_employee_required
@permission_required('stock.add_product',raise_exception=True)
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

@active_employee_required
@permission_required('stock.change_product',raise_exception=True)
def edit_product(req, pid):
    context = {
        'title': 'Editar Producto',
    }

    product = get_object_or_404(Product,pk=pid)

    if req.method == 'POST':
        form = AddProductForm(req.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product_detail', pid=product.id)
    else:
        form = AddProductForm(instance=product)

    context['form'] = form
    return render(req, 'forms/add_product.html', context)

@active_employee_required
@permission_required('stock.view_product',raise_exception=True)
def select_product(req):
    context = {
        'title': 'Seleccionar Producto'
    }

    if req.method == 'POST':
        form = SelectProductForm(req.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            product_id = product.pk
            return redirect('edit_product', pid=product_id)
    else:
        form = SelectProductForm()
    
    context['form'] = form
    return render(req, 'forms/select_product.html', context)

@active_employee_required
@permission_required('stock.view_product',raise_exception=False)
def product_autocomplete(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(name__icontains=q)
        results = [{'id': product.pk, 'text': product.name} for product in products]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

@active_employee_required
@permission_required('stock.add_record',raise_exception=True)
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

class RecordUpdateView(LoginRequiredMixin, ActiveEmployeeRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Record
    form_class = AddRecordForm
    template_name = 'forms/add_record.html'
    context_object_name = 'record'
    permission_required = 'stock.change_record'
    raise_exception = True
    success_url = reverse_lazy('record_list_filter')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        typeof = context['record'].typeof
        if typeof == Record.ENTRY:
            context['title'] = "Editar Ingreso"
        elif typeof == Record.EXIT:
            context['title'] = "Editar Egreso"

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = get_object_or_404(Employee, user=self.request.user)
        return kwargs

class BaseRecordsListView(LoginRequiredMixin, ActiveEmployeeRequiredMixin, PermissionRequiredMixin, ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'pages/record_list.html'
    permission_required = 'stock.view_record'
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        return Record.objects.order_by('-date')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            return redirect('index')  # Redirigir

        context['employee'] = employee

        return context

class RecordsForCurrentBranch(BaseRecordsListView):
    def get_queryset(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            return Record.objects.none()

        return Record.objects.filter(branch=employee.branch).order_by('-date')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Últimos Registros de {context['employee'].branch.name}"
        context['order'] = 'branch'
        context['btn_order'] = {'url': reverse('record_list'), 'label': 'Últimos Registros'}
        return context

class RecordsByTime(BaseRecordsListView):
    def get_queryset(self):
        return Record.objects.order_by('-date')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Últimos Registros (Hora)'
        context['order'] = 'time'
        context['btn_order'] = {'url': reverse('record_list_branch'), 'label': 'Registros de Sucursal'}
        return context
    
@active_employee_required
@permission_required('stock.view_record',raise_exception=True)
def record_list_filter(request):
    records = Record.objects.all().order_by('-date')
    record_filter = RecordFilter(request.GET, queryset=records)
    filtered_records = record_filter.qs

    paginator = Paginator(filtered_records, 10)  # 10 registros por página
    page = request.GET.get('page')
    
    try:
        paginated_records = paginator.page(page)
    except PageNotAnInteger:
        paginated_records = paginator.page(1)
    except EmptyPage:
        paginated_records = paginator.page(paginator.num_pages)

    context = {
        'title': 'Lista de Registros',
        'records': paginated_records,
        'filter': record_filter
    }

    return render(request, 'pages/record_list_filter.html', context)

@active_employee_required
@permission_required('stock.add_branch',raise_exception=True)
def register_branch(req):
    context = {
        'title': 'Registrar Sucursal',
        'submit_btn': 'Registrar'
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

@active_employee_required
@permission_required('stock.change_branch',raise_exception=True)
def edit_branch(req,branch_name):
    branch = get_object_or_404(Branch,name=branch_name)

    context = {
        'title': 'Actualizar Sucursal',
        'submit_btn': 'Actualizar'
    }

    if req.method == 'POST':
        form = RegisterBranch(req.POST,instance=branch)

        if form.is_valid():
            form.save()
            messages.success(req, '¡La sucursal se actualizó con exito!')
            return redirect('branch_list')
    else:
        form = RegisterBranch(instance=branch)
    
    context['form'] = form

    return render(req, 'forms/register_branch.html', context)

@active_employee_required
@permission_required('stock.view_branch',raise_exception=True)
def select_branch(req):
    context = {
        'title': 'Seleccionar Sucursal',
        'submit_btn': 'Editar'
    }

    if req.method == 'POST':
        form = SelectBranchForm(req.POST)

        if form.is_valid():
            branch = form.cleaned_data['branch']
            branch_name = branch.name
            return redirect('edit_branch', branch_name=branch_name)
    else:
        form = SelectBranchForm()
    
    context['form'] = form

    return render(req, 'forms/register_branch.html', context)


@active_employee_required
@permission_required('stock.view_branch',raise_exception=True)
def branch_list(req):
    branches = Branch.objects.all()
    context = {
        'title': 'Sucursales',
        'branches': branches
    }

    return render(req, 'pages/branch_list.html', context)

@active_employee_required
@permission_required('stock.view_employee',raise_exception=True)
def employee_list(req):
    employees = Employee.objects.all()
    context = {
        'title': 'Empleados',
        'employees': employees
    }

    return render(req, 'pages/employee_list.html', context)

@active_employee_required
def stock_list(req):
    branches = Branch.objects.all()
    branch_stock_map = []

    for branch in branches:
        stock_items = BranchStock.objects.filter(branch=branch)
        branch_stock_map.append({
            'branch': branch,
            'stock_items': stock_items
        })

    context = {
        'title': 'Inventario general',
        'branch_stock_map': branch_stock_map
    }

    return render(req, 'pages/stock_list.html', context)

@active_employee_required
def branch_stock_list(req):
    employee = Employee.objects.get(user=req.user)
    branch = employee.branch
    stock = BranchStock.objects.filter(branch=branch)
    branch_stock_map = [{
        'branch': branch,
        'stock_items': stock
    }]
    context = {
        'title': 'Stock en la sucursal',
        'branch_stock_map': branch_stock_map
    }

    return render(req, 'pages/stock_list.html', context)

@active_employee_required
@permission_required('stock.change_employee', raise_exception=True)
def administrate(req):
    admin_links = [
        {
            'title': 'Productos',
            'links': [
                {'url': reverse('add_product'), 'label': 'Agregar Producto'},
                {'url': reverse('select_product'), 'label': 'Editar Producto'},
                {'url': reverse('product_list'), 'label': 'Ver Productos'}
            ]
        },
        {
            'title': 'Empleados',
            'links': [
                {'url': reverse('employee_list'), 'label': 'Ver Empleados'}
            ]
        },
        {
            'title': 'Sucursales',
            'links': [
                {'url': reverse('add_branch'), 'label': 'Agregar Sucursal'},
                {'url': reverse('select_branch'), 'label': 'Editar Sucursal'},
                {'url': reverse('branch_list'), 'label': 'Ver Sucursales'}
            ]
        },
        {
            'title': 'Registros',
            'links': [
                {'url': reverse('record_list'), 'label': 'Agregar Registro'},
                {'url': reverse('record_list_filter'), 'label': 'Editar Registro'},
                {'url': reverse('record_list'), 'label': 'Ver Registros'}
            ]
        },
        {
            'title': 'Inventario',
            'links': [
                {'url': reverse('record_list'), 'label': 'Agregar Item'},
                {'url': reverse('record_list'), 'label': 'Editar Item'},
                {'url': reverse('stock_list'), 'label': 'Ver Inventarios'}
            ]
        },
    ]

    context = {
        'title': 'Administrar',
        'admin_links': admin_links
    }

    return render(req, 'pages/admin_page.html', context)

@login_required
@permission_required('stock.view_employee', raise_exception=True)
def employee_detail(req, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {
        'title': 'Datos de empleado',
        'employee': employee
    }

    return render(req, 'pages/employee_detail.html', context)

@login_required
@permission_required('stock.change_employee', raise_exception=True)
def edit_employee(req, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {
        'title': 'Actualizar empleado'
    }
    
    if req.method == 'POST':
        form = EditEmployeeForm(req.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        form = EditEmployeeForm(instance=employee)
    
    context['form'] = form
    return render(req, 'forms/register_employee.html', context)

@login_required
@permission_required('stock.change_employee', raise_exception=True)
def toggle_employee(req, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.is_active = not employee.is_active
    employee.save()
    return redirect('employee_detail', employee_id=employee.id)

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