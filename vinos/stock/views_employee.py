from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from .models import Branch,Employee
from .decorators import active_employee_required
from .forms import EditEmployeeForm

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
@permission_required('stock.view_employee', raise_exception=True)
def employee_detail(req, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {
        'title': 'Datos de empleado',
        'employee': employee
    }

    return render(req, 'pages/employee_detail.html', context)

@active_employee_required
@permission_required('stock.view_employee',raise_exception=True)
def employee_at_branch_list(req, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    employees = Employee.objects.filter(branch=branch)
    context = {
        'title': f'Empleados en {branch}',
        'employees': employees
    }

    return render(req, 'pages/employee_list.html', context)

@active_employee_required
@permission_required('stock.view_employee', raise_exception=False)
def employee_autocomplete(request):
    if 'q' in request.GET:
        q = request.GET['q']
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q)
        )
        results = [{'id': employee.pk, 'text': employee.full_name()} for employee in employees]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

@active_employee_required
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

@active_employee_required
@permission_required('stock.change_employee', raise_exception=True)
def toggle_employee(req, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.is_active = not employee.is_active
    employee.save()
    return redirect('employee_detail', employee_id=employee.id)
