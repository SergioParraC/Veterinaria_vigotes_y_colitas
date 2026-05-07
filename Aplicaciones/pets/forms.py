from django import forms
from . import models


class DuenoForm(forms.ModelForm):
    class Meta:
        model = models.Dueño
        fields = ['nombre', 'telefono', 'direccion', 'email']
        labels = {
            'nombre': 'Nombre del dueño',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'email': 'Correo electrónico',
        }


class MascotaForm(forms.ModelForm):
    class Meta:
        model = models.Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'peso', 'vacunado']
        labels = {
            'nombre': 'Nombre de la mascota',
            'especie': 'Especie',
            'raza': 'Raza',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'peso': 'Peso',
            'vacunado': 'Vacunado',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class CitaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label='Fecha de la cita',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = models.Cita
        fields = ['mascota', 'fecha', 'motivo', 'veterinario', 'estado']
        labels = {
            'mascota': 'Mascota',
            'fecha': 'Fecha de la cita',
            'motivo': 'Motivo',
            'veterinario': 'Veterinario',
            'estado': 'Estado',
        }


class VacunaForm(forms.ModelForm):
    class Meta:
        model = models.Vacuna
        fields = ['mascota', 'nombre_vacuna', 'fecha_aplicacion', 'veterinario']
        labels = {
            'mascota': 'Mascota',
            'nombre_vacuna': 'Nombre de la vacuna',
            'fecha_aplicacion': 'Fecha de aplicación',
            'veterinario': 'Veterinario',
        }
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
        }


class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = models.HistorialMedico
        fields = ['mascota', 'alergias', 'fecha_visita', 'motivo_visita', 'diagnostico', 'tratamiento']
        labels = {
            'mascota': 'Mascota',
            'alergias': 'Alergias',
            'fecha_visita': 'Fecha de visita',
            'motivo_visita': 'Motivo de visita',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
        }
        widgets = {
            'fecha_visita': forms.DateInput(attrs={'type': 'date'}),
        }
