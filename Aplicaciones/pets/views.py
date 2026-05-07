from datetime import date
from django.shortcuts import redirect, render
from Aplicaciones.veterinary import models as veterinary_models
from . import forms, models

def home_pets(request):
    data = {
        'titlePage': 'Mascotas',
        'titulo': 'Gestión de mascotas',
        'total_duenos': models.Dueño.objects.count(),
        'total_mascotas': models.Mascota.objects.count(),
        'total_citas': veterinary_models.Cita.objects.count(),
        'total_vacunas': models.Vacuna.objects.count(),
        'total_historiales': models.HistorialMedico.objects.count(),
        'mascotas': models.Mascota.objects.select_related('dueño').all().order_by('-id')[:10],
    }
    return render(request, 'pets-home.html', data)


def historia_mascota(request, id_mascota):
    mascota = models.Mascota.objects.get(pk=id_mascota)
    citas = veterinary_models.Cita.objects.select_related('cliente', 'mascota').filter(
        mascota=mascota,
    ).order_by('-fecha_cita', '-hora_cita')
    data = {
        'titlePage': f'Historia de {mascota.nombre}',
        'titulo': f'Historia de {mascota.nombre}',
        'mascota': mascota,
        'citas': citas,
        'vacunas': models.Vacuna.objects.filter(mascota=mascota).order_by('-fecha_aplicacion'),
        'historiales': models.HistorialMedico.objects.filter(mascota=mascota).order_by('-fecha_visita'),
    }
    return render(request, 'pets-historia.html', data)


def registrar_mascota(request):
    if request.method == 'POST':
        formulario_dueno = forms.DuenoForm(request.POST)
        formulario_mascota = forms.MascotaForm(request.POST)
        if formulario_dueno.is_valid() and formulario_mascota.is_valid():
            dueno = formulario_dueno.save()
            mascota = formulario_mascota.save(commit=False)
            mascota.dueño = dueno
            mascota.edad = calcular_edad(mascota.fecha_nacimiento)
            mascota.save()
            return redirect('/pets/')
    else:
        formulario_dueno = forms.DuenoForm()
        formulario_mascota = forms.MascotaForm()
    data = {
        'titlePage': 'Registrar dueño y mascota',
        'titulo': 'Registrar dueño y mascota',
        'formulario_dueno': formulario_dueno,
        'formulario_mascota': formulario_mascota,
        'boton': 'Guardar registro',
        'url_cancelar': '/pets/',
    }
    return render(request, 'pets-mascota-form.html', data)


def editar_mascota(request, id_mascota):
    mascota = models.Mascota.objects.get(pk=id_mascota)
    dueno = mascota.dueño

    if request.method == 'POST':
        formulario_dueno = forms.DuenoForm(request.POST, instance=dueno)
        formulario_mascota = forms.MascotaForm(request.POST, instance=mascota)
        if formulario_dueno.is_valid() and formulario_mascota.is_valid():
            formulario_dueno.save()
            mascota = formulario_mascota.save(commit=False)
            mascota.dueño = dueno
            mascota.edad = calcular_edad(mascota.fecha_nacimiento)
            mascota.save()
            return redirect(f'/pets/mascotas/{mascota.id}/historia/')
    else:
        formulario_dueno = forms.DuenoForm(instance=dueno)
        formulario_mascota = forms.MascotaForm(instance=mascota)

    data = {
        'titlePage': 'Editar dueño y mascota',
        'titulo': 'Editar dueño y mascota',
        'formulario_dueno': formulario_dueno,
        'formulario_mascota': formulario_mascota,
        'boton': 'Actualizar registro',
        'url_cancelar': f'/pets/mascotas/{mascota.id}/historia/',
    }
    return render(request, 'pets-mascota-form.html', data)


def calcular_edad(fecha_nacimiento):
    if not fecha_nacimiento:
        return 0
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def registrar_vacuna(request):
    if request.method == 'POST':
        formulario = forms.VacunaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('/pets/')
    else:
        formulario = forms.VacunaForm()
    data = {
        'titlePage': 'Registrar vacuna',
        'titulo': 'Registrar vacuna',
        'formulario': formulario,
        'boton': 'Guardar vacuna',
        'url_cancelar': '/pets/',
    }
    return render(request, 'pets-form.html', data)


def editar_vacuna(request, id_vacuna):
    vacuna = models.Vacuna.objects.get(pk=id_vacuna)

    if request.method == 'POST':
        formulario = forms.VacunaForm(request.POST, instance=vacuna)
        if formulario.is_valid():
            vacuna = formulario.save()
            return redirect(f'/pets/mascotas/{vacuna.mascota.id}/historia/')
    else:
        formulario = forms.VacunaForm(instance=vacuna)

    data = {
        'titlePage': 'Editar vacuna',
        'titulo': 'Editar vacuna',
        'formulario': formulario,
        'boton': 'Actualizar vacuna',
        'url_cancelar': f'/pets/mascotas/{vacuna.mascota.id}/historia/',
    }
    return render(request, 'pets-form.html', data)


def registrar_historial(request):
    if request.method == 'POST':
        formulario = forms.HistorialMedicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('/pets/')
    else:
        formulario = forms.HistorialMedicoForm()
    data = {
        'titlePage': 'Registrar historial médico',
        'titulo': 'Registrar historial médico',
        'formulario': formulario,
        'boton': 'Guardar historial',
        'url_cancelar': '/pets/',
    }
    return render(request, 'pets-form.html', data)


def editar_historial(request, id_historial):
    historial = models.HistorialMedico.objects.get(pk=id_historial)

    if request.method == 'POST':
        formulario = forms.HistorialMedicoForm(request.POST, instance=historial)
        if formulario.is_valid():
            historial = formulario.save()
            return redirect(f'/pets/mascotas/{historial.mascota.id}/historia/')
    else:
        formulario = forms.HistorialMedicoForm(instance=historial)

    data = {
        'titlePage': 'Editar historial médico',
        'titulo': 'Editar historial médico',
        'formulario': formulario,
        'boton': 'Actualizar historial',
        'url_cancelar': f'/pets/mascotas/{historial.mascota.id}/historia/',
    }
    return render(request, 'pets-form.html', data)
