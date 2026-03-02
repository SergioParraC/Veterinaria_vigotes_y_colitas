from django.db import models

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return 'Contacto de {self.nombre} - {self.email}'
