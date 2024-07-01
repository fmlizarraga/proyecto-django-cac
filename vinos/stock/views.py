from django.shortcuts import render

from .views_admin import administrate
from .views_auth import register_user,login_user,logout_user,inactive_user
from .views_branch import branch_list, register_branch, edit_branch, select_branch
from .views_employee import employee_list, employee_at_branch_list, employee_detail, employee_autocomplete, edit_employee, toggle_employee
from .views_inventory import stock_list, branch_stock_list, current_branch_stock_list, get_product_stock, edit_branch_stock
from .views_product import ProductList, product_detail, add_product, edit_product, select_product, product_autocomplete
from .views_record import RecordsForCurrentBranch, RecordsByTime, RecordUpdateView, add_record, record_list_filter

def index(req):
    context = {
        'title': 'Control de stock'
    }

    return render(req, 'pages/index.html', context)
