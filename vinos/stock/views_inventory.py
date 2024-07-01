from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Product,Branch,BranchStock,Employee
from .decorators import active_employee_required
from .forms import SelectBranchForm,BranchStockForm

@active_employee_required
def stock_list(req):
    form = SelectBranchForm(req.GET or None)
    branch_stock = None
    paginator = None

    if form.is_valid():
        branch = form.cleaned_data.get('branch')
        if branch:
            num_employees = Employee.objects.filter(branch=branch).count()
            num_products = BranchStock.objects.filter(branch=branch).count()

            stock_items = BranchStock.objects.filter(branch=branch).order_by('product')
            paginator = Paginator(stock_items, 8)

            page = req.GET.get('page')
            try:
                stock_items = paginator.page(page)
            except PageNotAnInteger:
                stock_items = paginator.page(1)
            except EmptyPage:
                stock_items = paginator.page(paginator.num_pages)

            branch_stock = {
                'branch': branch,
                'stock_items': stock_items,
                'num_employees': num_employees,
                'num_products': num_products
            }

    context = {
        'title': 'Inventario general',
        'form': form,
        'branch_stock': branch_stock,
        'paginator': paginator,
    }

    return render(req, 'pages/stock_list.html', context)

@active_employee_required
def branch_stock_list(req, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    stock_items = BranchStock.objects.filter(branch=branch).order_by('product')

    num_employees = Employee.objects.filter(branch=branch).count()
    num_products = BranchStock.objects.filter(branch=branch).count()

    paginator = Paginator(stock_items, 8)
    page = req.GET.get('page')
    try:
        stock_items = paginator.page(page)
    except PageNotAnInteger:
        stock_items = paginator.page(1)
    except EmptyPage:
        stock_items = paginator.page(paginator.num_pages)
    branch_stock = {
        'branch': branch,
        'stock_items': stock_items,
        'num_employees': num_employees,
        'num_products': num_products
    }
    context = {
        'title': 'Stock en la sucursal',
        'branch_stock': branch_stock,
        'paginator': paginator,
    }

    return render(req, 'pages/stock_list.html', context)

@active_employee_required
def current_branch_stock_list(req):
    employee = Employee.objects.get(user=req.user)
    branch = employee.branch

    num_employees = Employee.objects.filter(branch=branch).count()
    num_products = BranchStock.objects.filter(branch=branch).count()

    stock_items = BranchStock.objects.filter(branch=branch).order_by('product')
    paginator = Paginator(stock_items, 8)
    page = req.GET.get('page')
    try:
        stock_items = paginator.page(page)
    except PageNotAnInteger:
        stock_items = paginator.page(1)
    except EmptyPage:
        stock_items = paginator.page(paginator.num_pages)
    branch_stock = {
        'branch': branch,
        'stock_items': stock_items,
        'num_employees': num_employees,
        'num_products': num_products
    }
    context = {
        'title': 'Stock en la sucursal',
        'branch_stock': branch_stock,
        'paginator': paginator,
    }

    return render(req, 'pages/stock_list.html', context)

@active_employee_required
def get_product_stock(req, branch_name, product_id):
    branch = get_object_or_404(Branch,name=branch_name)
    product = get_object_or_404(Product,pk=product_id)
    try:
        branch_stock = BranchStock.objects.get(branch=branch,product=product)
        stock = branch_stock.stock
    except BranchStock.DoesNotExist:
        stock = 0
    return JsonResponse({'stock': stock})

@active_employee_required
def edit_branch_stock(req, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    
    if req.method == "POST":
        form = BranchStockForm(req.POST, branch=branch)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = BranchStockForm(branch=branch)
    
    context = {
        'title': f"Editar Stock de producto en {branch.name}",
        'form': form,
        'branch': branch
    }
    return render(req, 'forms/select_product.html', context)
