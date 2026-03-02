from django.db import models

# Create your models here.

class Dueño(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Mascota(models.Model):
    dueño = models.ForeignKey(Dueño, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vacunado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} {self.especie} ({self.dueño.nombre})'
    
class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales_medicos')
    alergias = models.TextField(blank=True)
    fecha_visita = models.DateField()
    motivo_visita = models.CharField(max_length=200)
    diagnostico = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return f'Historial médico de {self.mascota.nombre} - {self.fecha_visita}'
    
class Cita(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField()
    motivo = models.TextField(max_length=200)
    veterinario = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')])

    def __str__(self):
        return f'Cita de {self.mascota.nombre} - {self.fecha} - {self.estado}'

class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    veterinario = models.CharField(max_length=100)

    def __str__(self):
        return f'Vacuna {self.nombre} para {self.mascota.nombre} - Aplicada el {self.fecha_aplicacion} por {self.veterinario}'
    
