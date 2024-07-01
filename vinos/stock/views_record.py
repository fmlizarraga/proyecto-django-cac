
from typing import Any
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView, UpdateView
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from .models import Record,BranchStock,Employee
from .decorators import active_employee_required,ActiveEmployeeRequiredMixin
from .filters import RecordFilter
from .forms import AddRecordForm

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

@active_employee_required
@permission_required('stock.view_record',raise_exception=True)
def record_list_filter(request):
    records = Record.objects.all().order_by('-date')
    record_filter = RecordFilter(request.GET, queryset=records)
    filtered_records = record_filter.qs

    paginator = Paginator(filtered_records, 10)
    page = request.GET.get('page')
    
    try:
        paginated_records = paginator.page(page)
    except PageNotAnInteger:
        paginated_records = paginator.page(1)
    except EmptyPage:
        paginated_records = paginator.page(paginator.num_pages)

    context = {
        'title': 'Administración de Registros',
        'records': paginated_records,
        'filter': record_filter
    }

    return render(request, 'pages/record_list_filter.html', context)
