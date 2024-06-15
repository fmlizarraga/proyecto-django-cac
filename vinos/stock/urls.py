from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.product_list, name='product_list'),
    path('product/<int:pid>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('record/add/<str:type>/', views.add_record, name='add_record'),
    path('branch/add/', views.register_branch, name='add_branch'),
    path('branch/list/', views.branch_list, name='branch_list'),
    path('employee/add/', views.register_employee, name='add_employee'),
    path('employee/list/', views.employee_list, name='employee_list'),
    path('admin/', views.administrate, name='admin_page'),
]