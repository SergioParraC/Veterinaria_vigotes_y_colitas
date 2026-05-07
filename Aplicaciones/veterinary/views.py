from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cita
from django.http import HttpResponse


def home_citas(request):
    citas = Cita.objects.all()
    total = citas.count()
    return render(request, 'citas-home.html', {
        'Citas': citas,
        'Total': total,
        'titulo': 'Todos las Citas',
        'titlePage': 'Citas'
    })


def crear_cita(request):
    if request.method == "POST":
        data = request.POST
        cita = Cita()
        cita.nombre_mascota = data.get("NombreMascota")
        cita.dueño_mascota = data.get("DueñoMascota")
        cita.dueño_telefono = data.get("TeléfonoDueño")
        cita.dueño_email = data.get("EmailDueño")
        cita.tipo = data.get("Tipo")
        cita.fecha_cita = data.get("FechaCita")
        cita.hora_cita = data.get("HoraCita")
        cita.estado = data.get("Estado")
        cita.sintomas = data.get("Sintomas")
        cita.notas = data.get("Notas")
        cita.save()
        messages.success(request, 'Cita creada correctamente.')
        return redirect('citas:detalle_cita', id_cita=cita.id)
    data = {
        'cita': None,
        'titulo': 'Crear Cita',
        'boton': 'Crear',
        'titlePage': 'Crear Cita'
    }
    return render(request, 'cita-detail.html', data)


def detalle_cita(request, id_cita):
    cita = Cita.objects.get(pk=id_cita)
    if request.method == "POST":
        data = request.POST
        cita.nombre_mascota = data.get("NombreMascota")
        cita.dueño_mascota = data.get("DueñoMascota")
        cita.dueño_telefono = data.get("TeléfonoDueño")
        cita.dueño_email = data.get("EmailDueño")

        cita.tipo = data.get("Tipo")
        cita.fecha_cita = data.get("FechaCita")
        cita.hora_cita = data.get("HoraCita")
        cita.estado = data.get("Estado")
        cita.sintomas = data.get("Sintomas")
        cita.notas = data.get("Notas")
        cita.save()
        return render(request, 'cita-detail.html', {
            'cita': cita,
            'titulo': 'Editar Cita',
            'boton': 'Actualizar',
            'mensaje': 'Cita editada exitosamente',
            'titlePage': 'Editar Cita'
        })
    
    return render(request, 'cita-detail.html', {
        'cita': cita,
        'titulo': 'Editar Cita',
        'boton': 'Actualizar',
        'titlePage': 'Editar Cita'
    })


def buscar_cita(request):
    data = {
        'titlePage': 'Filtrar Citas'
    }
    return render(request, 'cita-search.html', data)


def filtrar_citas(request):
    citas = Cita.objects.all()
    nombre = request.GET.get('nombre', '').strip()
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    if nombre:
        citas = citas.filter(nombre_mascota__icontains=nombre)
    if tipo:
        citas = citas.filter(tipo=tipo)
    if estado:
        citas = citas.filter(estado=estado)
    total = citas.count()
    return render(request, 'citas-home.html', {
        'Citas': citas,
        'Total': total,
        'titulo': 'Resultados de búsqueda'
    })


def eliminar_cita(request, id_cita):
    try:
        cita = Cita.objects.get(pk=id_cita)
        cita.delete()
        messages.success(request, 'Cita eliminada exitosamente.')
    except Cita.DoesNotExist:
        messages.error(request, 'La cita no existe o ya fue eliminada.')
    return redirect('citas:listado_citas')