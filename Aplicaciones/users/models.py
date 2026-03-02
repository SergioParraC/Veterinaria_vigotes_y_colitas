from django.db import models

# Create your models here.

class Perfil(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Usuario(models.Model):
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50, choices=[('CC', 'Cedula de Ciudadania'), 
                                                              ('TI', 'Tarjeta de Identidad'), 
                                                              ('CE', 'Cedula de Extranjeria'), 
                                                              ('Otro', 'Otro')])
    numero_documento = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    rol = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.correo}'

class Cuenta_Usuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
    nombre_usuario = models.CharField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=128)
    estado = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])

    def __str__(self):
        return self.nombre_usuario