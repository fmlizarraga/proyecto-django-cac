from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Product
from .decorators import active_employee_required
from .filters import ProductFilter
from .forms import AddProductForm,SelectProductForm

class ProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-vintage', 'name']
    template_name = 'pages/product_list.html'
    permission_required = 'stock.view_product'
    raise_exception = True
    paginate_by = 9
    paginate_orphans = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vinos disponibles'
        context['filterset'] = self.filterset
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
