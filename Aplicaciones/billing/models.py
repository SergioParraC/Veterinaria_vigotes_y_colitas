from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.nombre
    
class Mascota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.nombre} ({self.cliente.nombre})'
    
class Servicio(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.tipo} - {self.descripcion}'
    
class Factura(models.Model):
    cliente_nombre = models.CharField(max_length=100,default='No disponible')
    cliente_telefono = models.CharField(max_length=20, default='No disponible')
    cliente_direccion = models.CharField(max_length=200, default='Sin dirección')
    cliente_email = models.CharField(max_length=200, default='sin_email@ejemplo.com')

    mascota_nombre = models.CharField(max_length=100,default='No disponible')
    mascota_especie = models.CharField(max_length=50,default='No disponible')
    mascota_raza = models.CharField(max_length=50,default='No disponible')
    mascota_edad = models.CharField(max_length=10,default='No disponible')

    servicio_descripcion = models.CharField(max_length=200, default='No disponible')
    servicio_cantidad = models.IntegerField(default=1)
    servicio_precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura de {self.cliente_nombre} - Total: ${self.total}"
