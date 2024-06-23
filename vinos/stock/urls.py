from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('product/<int:pid>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/select/', views.select_product, name='select_product'),
    path('product/edit/<int:pid>/', views.edit_product, name='edit_product'),
    path('record/add/<str:type>/', views.add_record, name='add_record'),
    path('record/list/', views.RecordsByTime.as_view(), name='record_list'),
    path('record/list/branch/', views.RecordsByBranch.as_view(), name='record_list_branch'),
    path('branch/add/', views.register_branch, name='add_branch'),
    path('branch/list/', views.branch_list, name='branch_list'),
    path('employee/list/', views.employee_list, name='employee_list'),
    path('stock/list/', views.stock_list, name='stock_list'),
    path('stock/list/current/', views.branch_stock_list, name='stock_list_curr'),
    path('admin/', views.administrate, name='admin_page'),
    path('product-autocomplete/', views.product_autocomplete, name='product-autocomplete'),
]