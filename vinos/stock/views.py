from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import Product
from .forms import AddProductForm, AddRecordForm

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
    if type == 'entry':
        title = 'Registrar Entrada'
    elif type == 'exit':
        title = 'Registrar Salida'
    else:
        raise Http404("Tipo de registro no válido")

    context = {
        'title': title,
    }
    
    if req.method == 'POST':
        form = AddRecordForm(req.POST)

        if form.is_valid():
            # TODO: accion en base de datos (dependiendo si es type entry o exit)

            messages.success(req, '¡Entrada/Salida registrada con exito!')
            return redirect('product_list')
    else:
        form = AddRecordForm()
        
    context['form'] = form
    return render(req, 'forms/add_record.html', context)