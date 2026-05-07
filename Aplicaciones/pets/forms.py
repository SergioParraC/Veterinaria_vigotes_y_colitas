from django import forms
from . import models


class SeleccionarDuenoForm(forms.Form):
    cliente = forms.ModelChoiceField(
        label="Cliente",
        queryset=models.Dueño.objects.all(),
        empty_label="Selecciona un cliente"
    )


class SeleccionarMascotaForm(forms.Form):
    mascota = forms.ModelChoiceField(
        label="Mascota",
        queryset=models.Mascota.objects.none(),
        empty_label="Selecciona la mascota",
        required=False
    )


class DuenoForm(forms.Form):
    nombre = forms.CharField(label="Nombre del dueño", max_length=100)
    telefono = forms.CharField(label="Teléfono", max_length=20)
    direccion = forms.CharField(label="Dirección", max_length=200, required=False)
    email = forms.EmailField(label="Correo electrónico", required=False)

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        initial = kwargs.get('initial', {})
        if instance:
            initial.update({
                'nombre': instance.nombre,
                'telefono': instance.telefono,
                'direccion': instance.direccion,
                'email': instance.email,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self):
        dueno = self.instance or models.Dueño()
        dueno.nombre = self.cleaned_data['nombre']
        dueno.telefono = self.cleaned_data['telefono']
        dueno.direccion = self.cleaned_data['direccion']
        dueno.email = self.cleaned_data['email']
        dueno.save()
        return dueno


class MascotaForm(forms.Form):
    nombre = forms.CharField(label="Nombre de la mascota", max_length=100)
    especie = forms.CharField(label="Especie", max_length=50)
    raza = forms.CharField(label="Raza", max_length=50)
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    peso = forms.DecimalField(label="Peso", max_digits=5, decimal_places=2, required=False)
    vacunado = forms.BooleanField(label="Vacunado", required=False)

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        initial = kwargs.get('initial', {})
        if instance:
            initial.update({
                'nombre': instance.nombre,
                'especie': instance.especie,
                'raza': instance.raza,
                'fecha_nacimiento': instance.fecha_nacimiento,
                'peso': instance.peso,
                'vacunado': instance.vacunado,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        mascota = self.instance or models.Mascota()
        mascota.nombre = self.cleaned_data['nombre']
        mascota.especie = self.cleaned_data['especie']
        mascota.raza = self.cleaned_data['raza']
        mascota.fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        mascota.peso = self.cleaned_data['peso']
        mascota.vacunado = self.cleaned_data['vacunado']
        if commit:
            mascota.save()
        return mascota


class VacunaForm(forms.Form):
    mascota = forms.ModelChoiceField(
        label="Mascota",
        queryset=models.Mascota.objects.all(),
        empty_label="Selecciona la mascota"
    )
    nombre_vacuna = forms.CharField(label="Nombre de la vacuna", max_length=100)
    fecha_aplicacion = forms.DateField(
        label="Fecha de aplicación",
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    veterinario = forms.CharField(label="Veterinario", max_length=100)

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        initial = kwargs.get('initial', {})
        if instance:
            initial.update({
                'mascota': instance.mascota,
                'nombre_vacuna': instance.nombre_vacuna,
                'fecha_aplicacion': instance.fecha_aplicacion,
                'veterinario': instance.veterinario,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self):
        vacuna = self.instance or models.Vacuna()
        vacuna.mascota = self.cleaned_data['mascota']
        vacuna.nombre_vacuna = self.cleaned_data['nombre_vacuna']
        vacuna.fecha_aplicacion = self.cleaned_data['fecha_aplicacion']
        vacuna.veterinario = self.cleaned_data['veterinario']
        vacuna.save()
        return vacuna


class HistorialMedicoForm(forms.Form):
    mascota = forms.ModelChoiceField(
        label="Mascota",
        queryset=models.Mascota.objects.all(),
        empty_label="Selecciona la mascota"
    )
    alergias = forms.CharField(label="Alergias", required=False, widget=forms.Textarea)
    fecha_visita = forms.DateField(
        label="Fecha de visita",
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    motivo_visita = forms.CharField(label="Motivo de visita", max_length=200)
    diagnostico = forms.CharField(label="Diagnóstico", widget=forms.Textarea)
    tratamiento = forms.CharField(label="Tratamiento", widget=forms.Textarea)

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        initial = kwargs.get('initial', {})
        if instance:
            initial.update({
                'mascota': instance.mascota,
                'alergias': instance.alergias,
                'fecha_visita': instance.fecha_visita,
                'motivo_visita': instance.motivo_visita,
                'diagnostico': instance.diagnostico,
                'tratamiento': instance.tratamiento,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self):
        historial = self.instance or models.HistorialMedico()
        historial.mascota = self.cleaned_data['mascota']
        historial.alergias = self.cleaned_data['alergias']
        historial.fecha_visita = self.cleaned_data['fecha_visita']
        historial.motivo_visita = self.cleaned_data['motivo_visita']
        historial.diagnostico = self.cleaned_data['diagnostico']
        historial.tratamiento = self.cleaned_data['tratamiento']
        historial.save()
        return historial
