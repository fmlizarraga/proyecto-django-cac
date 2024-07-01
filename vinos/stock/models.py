from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime

def validate_positive(value):
    if value <= 0:
        raise ValidationError("El valor debe ser positivo")

class Person(models.Model):
    dni = models.IntegerField(
        verbose_name="DNI", 
        unique=True,
        validators=[validate_positive]
    )

    class Meta:
        abstract = True

class Branch(models.Model):
    name = models.CharField(
        max_length=255, 
        verbose_name="Sucursal",
        unique=True,
        validators=[RegexValidator(r'^\S+', 'Este campo no puede estar vacío.')]
    )
    address = models.CharField(
        max_length=255, 
        verbose_name="Direccion",
        validators=[RegexValidator(r'^\S+', 'Este campo no puede estar vacío.')]
    )
    telephone = models.CharField(
        max_length=100, 
        verbose_name="Telefono",
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono no válido.')]
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    MALBEC = 'Malbec'
    CABERNET = 'Cabernet'
    MERLOT = 'Merlot'
    CHARDONNAY = 'Chardonnay'
    SYRAH = 'Syrah'
    PINOT_NOIR = 'Pinot Noir'
    SAUVIGNON_BLANC = 'Sauvignon Blanc'
    
    VARIETY_CHOICES = [
        (MALBEC, 'Malbec'),
        (CABERNET, 'Cabernet'),
        (MERLOT, 'Merlot'),
        (CHARDONNAY, 'Chardonnay'),
        (SYRAH, 'Syrah'),
        (PINOT_NOIR, 'Pinot Noir'),
        (SAUVIGNON_BLANC, 'Sauvignon Blanc'),
    ]

    name = models.CharField(
        max_length=100, 
        verbose_name="Nombre"
    )
    variety = models.CharField(
        max_length=20,
        choices=VARIETY_CHOICES,
        verbose_name="Varietal"
    )
    description = models.TextField(
        max_length=500, 
        verbose_name="Descripcion"
    )
    vintage = models.IntegerField(
        verbose_name="Cosecha",
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)]
    )
    branches = models.ManyToManyField(Branch, through='BranchStock', verbose_name="Sucursales")

    def __str__(self):
        return f"Cod.: {self.pk} - {self.name} - {self.variety} {self.vintage}"

class BranchStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='branch_stocks')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_stocks')
    stock = models.IntegerField(verbose_name="Stock en Sucursal", default=0)

    def __str__(self):
        return f"Sucursal: {self.branch.name} - Producto: {self.product.name} - Stock: {self.stock}"


class Employee(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name="employee")
    is_active = models.BooleanField(
        verbose_name="En actividad",
        default=True
    )
    cuil = models.CharField(
        verbose_name="CUIL", 
        unique=True,
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\d{2}-\d{7,8}-\d$',
                message='El CUIL debe estar en el formato NN-NNNNNNNN-N'
            )
        ]
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Sucursal")

    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"Empleado: {self.user.get_full_name()} - DNI: {self.dni} - CUIL: {self.cuil} - Sucursal: {self.branch} - En actividad: {'Si' if self.is_active else 'No'}"

class Record(models.Model):
    ENTRY = 'entry'
    EXIT = 'exit'
    TYPE_CHOICES = [
        (ENTRY, 'Entry'),
        (EXIT, 'Exit')
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name="Cantidad",
        validators=[validate_positive]
    )
    typeof = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES,
        verbose_name="Tipo"
    )
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Empleado")
    date = models.DateTimeField(verbose_name="Fecha de registro", auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.name} - Branch: {self.branch.name} - Quantity: {self.quantity} - Type:{self.get_typeof_display()} - Employee: {self.employee.full_name()} - Date: {self.date}"
