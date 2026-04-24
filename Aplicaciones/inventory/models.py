from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la categoría')
    descripcion = models.TextField(max_length=250, blank=True, null=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre del proveedor')
    contacto = models.CharField(max_length=100, verbose_name='Contacto')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    direccion = models.TextField(verbose_name='Dirección')

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del producto')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos')
    descripcion = models.TextField(max_length=250, blank=True, null=True, verbose_name='Descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio unitario')
    stock = models.PositiveIntegerField(verbose_name='Cantidad disponible en stock')
    img = models.ImageField(blank=True, null=True, verbose_name='Imagen del producto')
    
    def __str__(self):
        return self.nombre