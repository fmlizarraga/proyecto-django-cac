from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime

def validate_positive(value):
    if value <= 0:
        raise ValidationError("El valor debe ser positivo")

class Person(models.Model):
    first_name = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        validators=[
            RegexValidator(r'^[a-zA-Z]+$', 'Solo se permiten caracteres alfabéticos.')
        ]
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Apellido",
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Solo se permiten caracteres alfabéticos.')]
    )
    dni = models.IntegerField(
        verbose_name="DNI", 
        unique=True,
        validators=[validate_positive]
    )

    class Meta:
        abstract = True
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Branch(models.Model):
    name = models.CharField(
        max_length=255, 
        verbose_name="Sucursal",
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
        return f"Nombre: {self.name} - Varietal: {self.variety} - Descripcion: {self.description} - Cosecha: {self.vintage}"

class BranchStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="Stock en Sucursal")

    def __str__(self):
        return f"Sucursal: {self.branch.name} - Producto: {self.product.name} - Stock: {self.stock}"


class Employee(Person):
    is_active = models.BooleanField(
        verbose_name="En actividad",
        default=True
    )
    cuil = models.IntegerField(
        verbose_name="CUIL", 
        unique=True,
        validators=[validate_positive]
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Sucursal")

    def __str__(self):
        return f"Empleado: {self.full_name()} - DNI: {self.dni} - CUIL: {self.cuil} - Sucursal: {self.branch} - En actividad: {'Si' if self.is_active else 'No'}"

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
    date = models.DateField(verbose_name="Fecha de registro", auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.name} - Branch: {self.branch.name} - Quantity: {self.quantity} - Type:{self.get_typeof_display()} - Employee: {self.employee.full_name()} - Date: {self.date}"
