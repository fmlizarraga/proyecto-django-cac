def company_info(request):
    return {
        'company_name': 'Bodega San Martín',
        'company_greeter': '''En Bodega San Martin, gestionamos con precisión y eficiencia nuestro inventario de vinos.
        Este sistema está diseñado exclusivamente para el uso del personal de la bodega,
        permite realizar registros detallados de entradas y salidas,
        así como consultar el inventario actual en cualquier momento.
        Nuestro objetivo es garantizar la mejor organización y control para ofrecer siempre
        la más alta calidad en nuestros productos.''',
        'company_msg': '¡Gracias por su dedicación y esfuerzo continuo!'
    }
