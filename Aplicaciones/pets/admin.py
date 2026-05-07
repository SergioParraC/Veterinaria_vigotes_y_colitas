from django.contrib import admin
from . import models

admin.site.register(models.Dueño)
admin.site.register(models.Mascota)
admin.site.register(models.HistorialMedico)
admin.site.register(models.Cita)
admin.site.register(models.Vacuna)
