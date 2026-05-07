from datetime import date
from django.shortcuts import redirect, render
from . import forms, models

def home_pets(request):
    data = {
        'titlePage': 'Mascotas',
        'titulo': 'Gestión de mascotas',
        'total_duenos': models.Dueño.objects.count(),
        'total_mascotas': models.Mascota.objects.count(),
        'total_citas': models.Cita.objects.count(),
        'total_vacunas': models.Vacuna.objects.count(),
        'total_historiales': models.HistorialMedico.objects.count(),
        'mascotas': models.Mascota.objects.select_related('dueño').all().order_by('-id')[:10],
    }
    return render(request, 'pets-home.html', data)


def historia_mascota(request, id_mascota):
    mascota = models.Mascota.objects.get(pk=id_mascota)
    data = {
        'titlePage': f'Historia de {mascota.nombre}',
        'titulo': f'Historia de {mascota.nombre}',
        'mascota': mascota,
        'citas': models.Cita.objects.filter(mascota=mascota).order_by('-fecha'),
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


def registrar_cita(request):
    if request.method == 'POST':
        formulario = forms.CitaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('/pets/')
    else:
        formulario = forms.CitaForm()
    data = {
        'titlePage': 'Registrar cita',
        'titulo': 'Registrar cita',
        'formulario': formulario,
        'boton': 'Guardar cita',
    }
    return render(request, 'pets-form.html', data)


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
    }
    return render(request, 'pets-form.html', data)
