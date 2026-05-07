from django.db import models

# Create your models here.

class Cita(models.Model):
    estado_fields = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),       
        
    ]
    
    tipo_fields = [
        ('Consulta', 'Consulta General'),
        ('Vacunación', 'Vacunación'),
        ('Cirugía', 'Cirugía'),
        ('Peluqueria', 'Peluqueria'),
        ('Control', 'Control'),
        ('Emergencia', 'Emergencia'),
        
    ]
    
    cliente = models.ForeignKey('pets.Dueño', on_delete=models.PROTECT, null=True, blank=True)
    mascota = models.ForeignKey('pets.Mascota', on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=tipo_fields, default= 'Consulta', verbose_name='Tipo de Cita')
    fecha_cita = models.DateTimeField(verbose_name='Fecha de la Cita')
    hora_cita = models.TimeField(verbose_name='Hora de la Cita')
    estado = models.CharField(max_length=20, choices=estado_fields, default='Pendiente', verbose_name='Estado de la Cita')
    sintomas = models.TextField(blank=True, null=True, verbose_name='Síntomas de la Mascota')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas Adicionales')
    