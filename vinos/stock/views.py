from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import Product,Branch,Record,BranchStock
from .forms import AddProductForm,AddRecordForm,RegisterBranch

def index(req):
    context = {
        'title': 'Control de stock'
    }

    return render(req, 'pages/index.html', context)

def product_list(req):
    products = Product.objects.all()
    context = {
        'title': 'Vinos disponibles',
        'stock': products
    }

    return render(req, 'pages/product_list.html', context)

def product_detail(req, pid):
    product = get_object_or_404(Product,pk=pid)

    context = {
        'title': 'Detalle de producto',
        'product': product
    }

    return render(req, 'pages/product_detail.html', context)

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

def add_record(req, type):
    TYPE_CHOICES = {
        'entry': Record.ENTRY,
        'exit': Record.EXIT,
    }

    if type not in TYPE_CHOICES:
        messages.error(req, 'Tipo de registro no válido.')
        return redirect('index')
    
    context = {}
    if type == TYPE_CHOICES['entry']:
        context['title'] = "Ingreso"
    elif type == TYPE_CHOICES['exit']:
        context['title'] = "Egreso"
    
    if req.method == 'POST':
        form = AddRecordForm(req.POST)

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
            return redirect('index')
        else:
            messages.error(req, 'Error al crear el registro. Verifique los datos ingresados.')
    else:
        form = AddRecordForm(initial={'typeof': TYPE_CHOICES[type]})

    context['form'] = form
    return render(req, 'forms/add_record.html', context)

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

def branch_list(req):
    branches = Branch.objects.all()
    context = {
        'title': 'Sucursales',
        'branches': branches
    }

    return render(req, 'pages/branch_list.html', context)