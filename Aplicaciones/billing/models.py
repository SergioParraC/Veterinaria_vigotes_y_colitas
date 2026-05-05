from django.db import models

class Factura(models.Model):
    ESTADO = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey('pets.Dueño', on_delete=models.PROTECT, null=True, blank=True)
    mascota = models.ForeignKey('pets.Mascota', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO, default='BORRADOR')

class FacturaDetalle(models.Model):
    TIPO = [
        ('CITA', 'Cita'),
        ('PRODUCTO', 'Producto'),
        ('OTRO', 'Otro'),
    ]
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    tipo = models.CharField(max_length=20, choices=TIPO)

    cita = models.ForeignKey('pets.Cita', on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.ForeignKey('inventory.Producto', on_delete=models.SET_NULL, null=True, blank=True)

    descripcion = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)