from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from stock.models import Employee

User = get_user_model()

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            employee = Employee.objects.get(user=user)
            if user.check_password(password) and employee.is_active:
                return user
        except User.DoesNotExist:
            return None
        except Employee.DoesNotExist:
            return None
