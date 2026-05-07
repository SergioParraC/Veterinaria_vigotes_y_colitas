from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cita
from django.http import HttpResponse
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa


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


def _generar_pdf(html_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    response.write(result_file.getvalue())
    return response


def generar_pdf_citas(request):
    citas = Cita.objects.all()
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    filas = ''
    for c in citas:
        fecha_fmt = c.fecha_cita.strftime('%d/%m/%Y') if c.fecha_cita else ''
        hora_fmt = c.hora_cita.strftime('%H:%M') if c.hora_cita else ''
        filas += f'''
        <tr>
            <td>{c.nombre_mascota}</td>
            <td>{c.dueno_mascota}</td>
            <td>{c.dueno_telefono}</td>
            <td>{c.dueno_email}</td>
            <td>{c.tipo}</td>
            <td>{fecha_fmt}</td>
            <td>{hora_fmt}</td>
            <td>{c.estado}</td>
        </tr>'''
    html = f'''
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Helvetica, sans-serif; font-size: 11px; }}
            h1 {{ color: #146105; text-align: center; }}
            .fecha {{ text-align: right; font-size: 10px; color: #666; margin-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #acffaf; color: #000; padding: 5px 6px; border: 1px solid #000; text-align: left; }}
            td {{ padding: 4px 6px; border: 1px solid #000; }}
            .total {{ margin-top: 10px; font-size: 13px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Listado de Citas</h1>
        <p class="fecha">Generado: {fecha}</p>
        <table>
            <thead>
                <tr>
                    <th>Mascota</th>
                    <th>Dueno</th>
                    <th>Telefono</th>
                    <th>Email</th>
                    <th>Tipo</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>{filas}</tbody>
        </table>
        <p class="total">Total de citas: {citas.count()}</p>
    </body>
    </html>'''
    return _generar_pdf(html, 'citas.pdf')