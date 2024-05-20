from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.product_list, name='product_list'),
    path('product/<int:pid>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
]