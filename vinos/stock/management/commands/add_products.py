from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from stock.models import Product

class Command(BaseCommand):
    help = 'Agregar una serie de productos de prueba a la base de datos.'

    def handle(self, *args, **kwargs):
        productos = [
            Product(name="Reserva Malbec", variety=Product.MALBEC, description="Un vino Malbec de reserva.", vintage=2020),
            Product(name="Gran Cabernet", variety=Product.CABERNET, description="Un excelente Cabernet.", vintage=2019),
            Product(name="Clásico Merlot", variety=Product.MERLOT, description="Un Merlot clásico y suave.", vintage=2021),
            Product(name="Chardonnay Premium", variety=Product.CHARDONNAY, description="Un Chardonnay de calidad premium.", vintage=2020),
            Product(name="Syrah Reserva", variety=Product.SYRAH, description="Un Syrah con cuerpo y estructura.", vintage=2018),
            Product(name="Pinot Noir Elegante", variety=Product.PINOT_NOIR, description="Un Pinot Noir elegante y delicado.", vintage=2019),
            Product(name="Viña del Sol", variety=Product.MALBEC, description="Un Malbec robusto con notas de ciruela y un toque de roble.", vintage=2019),
            Product(name="Castillo de la Luna", variety=Product.CABERNET, description="Cabernet intenso con aromas a mora y un final ahumado.", vintage=2020),
            Product(name="Reserva del Valle", variety=Product.MERLOT, description="Merlot suave con toques de cereza y chocolate oscuro.", vintage=2018),
            Product(name="Estrella Dorada", variety=Product.CHARDONNAY, description="Chardonnay refrescante con notas de manzana verde y vainilla.", vintage=2021),
            Product(name="La Cumbre", variety=Product.SYRAH, description="Syrah especiado con sabores a frutos rojos y un toque de pimienta.", vintage=2019),
            Product(name="Viñedos del Mar", variety=Product.PINOT_NOIR, description="Pinot Noir elegante con matices de frambuesa y tierra húmeda.", vintage=2020),
            Product(name="Bosque Encantado", variety=Product.SAUVIGNON_BLANC, description="Sauvignon Blanc fresco con aromas a cítricos y hierbas.", vintage=2021),
            Product(name="Altos del Plata", variety=Product.MALBEC, description="Malbec estructurado con sabores a mora y un final aterciopelado.", vintage=2018),
            Product(name="Campo de los Sueños", variety=Product.CABERNET, description="Cabernet complejo con notas de grosella negra y cuero.", vintage=2019),
            Product(name="Colina Verde", variety=Product.CHARDONNAY, description="Chardonnay afrutado con toques de melocotón y un acabado cremoso.", vintage=2020)
        ]

        try:
            Product.objects.bulk_create(productos)
            self.stdout.write(self.style.SUCCESS('Productos agregados exitosamente.'))
        except (IntegrityError, ValidationError) as e:
            self.stdout.write(self.style.ERROR(f'Error al agregar productos: {e}'))