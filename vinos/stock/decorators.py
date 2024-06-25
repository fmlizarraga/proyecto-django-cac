from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from functools import wraps

def active_employee_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        employee = getattr(request.user, 'employee', None)
        if employee is not None and employee.is_active:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('inactive_user')  # Redirige a una vista adecuada
    return _wrapped_view

def anonymous_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

class ActiveEmployeeRequiredMixin(View):
    @method_decorator(active_employee_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)