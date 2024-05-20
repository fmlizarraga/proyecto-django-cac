from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import AddProductForm, EntryForm, ExitForm

# ! Temporal
MY_STOCK = [
    {
        'id': 1,
        'name': 'Royal Red',
        'variety': 'Malbec',
        'description': 'Un vino suave con tonos frutados ideal para acompañar carnes rojas',
        'vintage': 2020,
        'quantity': 5
    },
    {
        'id': 2,
        'name': 'Golden Chardonnay',
        'variety': 'Chardonnay',
        'description': 'Un vino blanco fresco y afrutado, perfecto para mariscos y ensaladas',
        'vintage': 2019,
        'quantity': 20
    },
    {
        'id': 3,
        'name': 'Ancient Cabernet',
        'variety': 'Cabernet Sauvignon',
        'description': 'Un vino tinto robusto con notas de especias y roble, ideal para platos fuertes',
        'vintage': 2018,
        'quantity': 15
    },
    {
        'id': 4,
        'name': 'Summer Rosé',
        'variety': 'Rosé',
        'description': 'Un vino rosado refrescante con toques de fresa y cítricos, excelente para días calurosos',
        'vintage': 2021,
        'quantity': 30
    },
    {
        'id': 5,
        'name': 'Velvet Pinot Noir',
        'variety': 'Pinot Noir',
        'description': 'Un vino tinto elegante con aromas de frutas rojas y un final sedoso',
        'vintage': 2017,
        'quantity': 7
    }
]
# ! Temporal

# Create your views here.

def index(req):
    context = {
        'title': 'Control de stock'
    }

    return render(req, 'pages/index.html', context)

def product_list(req):
    context = {
        'title': 'Vinos disponibles',
        'stock': MY_STOCK
    }

    return render(req, 'pages/product_list.html', context)

def product_detail(req, pid):
    product = next((item for item in MY_STOCK if item["id"] == pid), None)

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
            # !TODO reemplazar esto por una operacion en base de datos!
            product_data = form.cleaned_data
            new_product = {
                'id': len(MY_STOCK) + 1,
                **product_data
            }
            MY_STOCK.append(new_product)

            messages.success(req, '¡El producto fue agregado al inventario con exito!')
            return redirect('product_list')
    else:
        form = AddProductForm()
    
    context['form'] = form
    return render(req, 'forms/add_product.html', context)