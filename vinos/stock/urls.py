from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # index
    path('', views.index, name='index'),
    # productos
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('product/<int:pid>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/select/', views.select_product, name='select_product'),
    path('product/edit/<int:pid>/', views.edit_product, name='edit_product'),
    # registros
    path('record/add/<str:type>/', views.add_record, name='add_record'),
    path('record/edit/<int:pk>/', views.RecordUpdateView.as_view(), name='edit_record'),
    path('record/list/', views.RecordsByTime.as_view(), name='record_list'),
    path('record/list/branch/', views.RecordsForCurrentBranch.as_view(), name='record_list_branch'),
    path('record/list/filter/', views.record_list_filter, name='record_list_filter'),
    # sucursales
    path('branch/select/<str:action>/', views.select_branch, name='select_branch'),
    path('branch/edit/<str:branch_name>/', views.edit_branch, name='edit_branch'),
    path('branch/add/', views.register_branch, name='add_branch'),
    path('branch/list/', views.branch_list, name='branch_list'),
    # empleados
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employee/list/', views.employee_list, name='employee_list'),
    path('employee/list/at/<int:branch_id>', views.employee_at_branch_list, name='employee_list_branch'),
    path('employee/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employee/toggle/<int:employee_id>/', views.toggle_employee, name='toggle_employee'),
    # inventarios
    path('stock/list/', views.stock_list, name='stock_list'),
    path('stock/list/current/', views.current_branch_stock_list, name='stock_list_curr'),
    path('stock/list/<int:branch_id>/', views.branch_stock_list, name='stock_list_branch'),
    path('branch/stock/edit/<str:branch_name>/', views.edit_branch_stock, name='edit_branch_stock'),
    # utilidades
    path('admin/', views.administrate, name='admin_page'),
    path('product-autocomplete/', views.product_autocomplete, name='product-autocomplete'),
    path('employee-autocomplete/', views.employee_autocomplete, name='employee-autocomplete'),
    path('get_product_stock/<str:branch_name>/<int:product_id>/', views.get_product_stock, name='get_product_stock'),
]