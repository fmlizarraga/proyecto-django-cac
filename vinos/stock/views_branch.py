from django.db.models import Count, Subquery, OuterRef
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Branch,BranchStock,Employee
from .decorators import active_employee_required
from .forms import RegisterBranch,SelectBranchForm

@active_employee_required
@permission_required('stock.view_branch', raise_exception=True)
def branch_list(request):
    employee_count = Employee.objects.filter(branch=OuterRef('pk')).values('branch').annotate(count=Count('id')).values('count')
    product_count = BranchStock.objects.filter(branch=OuterRef('pk')).values('branch').annotate(count=Count('id')).values('count')

    branches = Branch.objects.annotate(
        num_employees=Subquery(employee_count),
        num_products=Subquery(product_count)
    )

    context = {
        'title': 'Sucursales',
        'branches': branches
    }

    return render(request, 'pages/branch_list.html', context)

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
def select_branch(req,action):
    context = {
        'title': 'Seleccionar Sucursal',
        'submit_btn': 'Editar'
    }

    if req.method == 'POST':
        form = SelectBranchForm(req.POST)

        if form.is_valid():
            branch = form.cleaned_data['branch']
            branch_name = branch.name
            return redirect(action, branch_name=branch_name)
    else:
        form = SelectBranchForm()
    
    context['form'] = form

    return render(req, 'forms/register_branch.html', context)

