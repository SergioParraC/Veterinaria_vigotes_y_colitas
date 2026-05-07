from django.db import models

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    numero_contacto = models.CharField(max_length=20)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f'Contacto de {self.nombre} - {self.email}'
