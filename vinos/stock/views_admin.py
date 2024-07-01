from django.shortcuts import render
from django.urls import reverse
from .decorators import active_employee_required

@active_employee_required
def administrate(request):
    links_by_entity = {
        'Empleados': {
            'view_employee': [
                {'url': reverse('employee_list'), 'label': 'Administrar Empleados', 'icon_class': 'fa-solid fa-users-gear'}
            ]
        },
        'Registros': {
            'view_record': [
                {'url': reverse('record_list'), 'label': 'Gestión Básica de Registros', 'icon_class': 'fa-solid fa-file-alt'},
                {'url': reverse('record_list_filter'), 'label': 'Gestión Avanzada de Registros', 'icon_class': 'fa-solid fa-filter'}
            ]
        },
        'Productos': {
            'add_product': [
                {'url': reverse('add_product'), 'label': 'Agregar Producto', 'icon_class': 'fa-solid fa-plus'}
            ],
            'change_product': [
                {'url': reverse('select_product'), 'label': 'Editar Producto', 'icon_class': 'fa-solid fa-edit'}
            ],
            'view_product': [
                {'url': reverse('product_list'), 'label': 'Ver Productos', 'icon_class': 'fa-solid fa-eye'}
            ]
        },
        'Inventarios': {
            'change_branchstock': [
                {'url': reverse('select_branch', args=['edit_branch_stock']), 'label': 'Editar Inventario', 'icon_class': 'fa-solid fa-warehouse'}
            ],
            'view_branchstock': [
                {'url': reverse('stock_list'), 'label': 'Ver Inventarios', 'icon_class': 'fa-solid fa-boxes'}
            ]
        },
        'Sucursales': {
            'add_branch': [
                {'url': reverse('add_branch'), 'label': 'Agregar Sucursal', 'icon_class': 'fa-solid fa-building-circle-arrow-right'}
            ],
            'change_branch': [
                {'url': reverse('select_branch', args=['edit_branch']), 'label': 'Editar Sucursal', 'icon_class': 'fa-solid fa-building-circle-exclamation'}
            ],
            'view_branch': [
                {'url': reverse('branch_list'), 'label': 'Ver Sucursales', 'icon_class': 'fa-solid fa-building'}
            ]
        }
    }

    admin_links = []
    for entity, perms in links_by_entity.items():
        entity_links = []
        for perm, links in perms.items():
            if request.user.has_perm(f'stock.{perm}'):
                entity_links.extend(links)
        if entity_links:
            admin_links.append({
                'title': entity,
                'links': entity_links
            })

    context = {
        'title': 'Administrar',
        'admin_links': admin_links
    }

    return render(request, 'pages/admin_page.html', context)
