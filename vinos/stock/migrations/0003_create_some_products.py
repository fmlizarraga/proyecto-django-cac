from django.db import migrations, IntegrityError

def create_initial_data(apps, schema_editor):
    Branch = apps.get_model('stock', 'Branch')
    Employee = apps.get_model('stock', 'Employee')
    Product = apps.get_model('stock', 'Product')
    User = apps.get_model('auth', 'User')

    try:
        # Crear sucursales
        branch1, created1 = Branch.objects.get_or_create(name="Casa Central", defaults={"address": "Av. Principal 123", "telephone": "+541112345678"})
        branch2, created2 = Branch.objects.get_or_create(name="Sucursal Norte", defaults={"address": "Calle Secundaria 456", "telephone": "+541198765432"})

        # Crear usuarios
        user1, created_user1 = User.objects.get_or_create(username='empleado1', defaults={"email": 'juan@mail.com', "first_name": 'Juan', "last_name": 'Perez'})
        user2, created_user2 = User.objects.get_or_create(username='empleado2', defaults={"email": 'ana@mail.com', "first_name": 'Ana', "last_name": 'Gomez'})

        # Crear empleados si no existen
        if created_user1:
            employee1 = Employee(user=user1, dni=12345678, cuil='20-12345678-5', branch=branch1)
            employee1.save()

        if created_user2:
            employee2 = Employee(user=user2, dni=87654321, cuil='23-87654321-1', branch=branch2)
            employee2.save()

        # Crear productos
        productos = [
            Product(name="Reserva Malbec", variety="Malbec", description="Un vino Malbec de reserva.", vintage=2020),
            Product(name="Gran Cabernet", variety="Cabernet", description="Un excelente Cabernet.", vintage=2019),
            Product(name="Clásico Merlot", variety="Merlot", description="Un Merlot clásico y suave.", vintage=2021),
            Product(name="Chardonnay Premium", variety="Chardonnay", description="Un Chardonnay de calidad premium.", vintage=2020),
            Product(name="Syrah Reserva", variety="Syrah", description="Un Syrah con cuerpo y estructura.", vintage=2018),
            Product(name="Pinot Noir Elegante", variety="Pinot Noir", description="Un Pinot Noir elegante y delicado.", vintage=2019),
            Product(name="Viña del Sol", variety="Malbec", description="Un Malbec robusto con notas de ciruela y un toque de roble.", vintage=2019),
            Product(name="Castillo de la Luna", variety="Cabernet", description="Cabernet intenso con aromas a mora y un final ahumado.", vintage=2020),
            Product(name="Reserva del Valle", variety="Merlot", description="Merlot suave con toques de cereza y chocolate oscuro.", vintage=2018),
            Product(name="Estrella Dorada", variety="Chardonnay", description="Chardonnay refrescante con notas de manzana verde y vainilla.", vintage=2021),
            Product(name="La Cumbre", variety="Syrah", description="Syrah especiado con sabores a frutos rojos y un toque de pimienta.", vintage=2019),
            Product(name="Viñedos del Mar", variety="Pinot Noir", description="Pinot Noir elegante con matices de frambuesa y tierra húmeda.", vintage=2020),
            Product(name="Bosque Encantado", variety="Sauvignon Blanc", description="Sauvignon Blanc fresco con aromas a cítricos y hierbas.", vintage=2021),
            Product(name="Altos del Plata", variety="Malbec", description="Malbec estructurado con sabores a mora y un final aterciopelado.", vintage=2018),
            Product(name="Campo de los Sueños", variety="Cabernet", description="Cabernet complejo con notas de grosella negra y cuero.", vintage=2019),
            Product(name="Colina Verde", variety="Chardonnay", description="Chardonnay afrutado con toques de melocotón y un acabado cremoso.", vintage=2020)
        ]
        Product.objects.bulk_create(productos)
    except IntegrityError as e:
        print(f"Error de integridad al crear datos iniciales: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_branchstock_branch_alter_branchstock_product'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
