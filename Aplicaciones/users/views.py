from django.shortcuts import render, redirect
from . import models
from .forms import PerfilForm, UsuarioForm, CuentaUsuarioForm
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa


def home_perfiles(request):
    perfiles = models.Perfil.objects.all()
    total = perfiles.count()
    return render(request, 'perfil-home.html', {
        'Perfiles': perfiles,
        'Total': total,
        'titlePage': 'Listado Perfiles'
    })


def crear_perfil(request):
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save()
            messages.success(request, 'Perfil creado correctamente.')
            return redirect('users:editar_perfil', id_perfil=perfil.id)
    else:
        form = PerfilForm()
    return render(request, 'perfil-detail.html', {
        'form': form,
        'titulo': 'Crear perfil',
        'boton_text': 'Crear',
        'titlePage': 'Crear perfil'
    })


def editar_perfil(request, id_perfil):
    perfil = models.Perfil.objects.get(pk=id_perfil)
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'El perfil se ha actualizado correctamente.')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'perfil-detail.html', {
        'form': form,
        'perfil': perfil,
        'titulo': 'Editar perfil',
        'boton_text': 'Actualizar',
        'titlePage': 'Editar perfil'
    })


def home_usuarios(request):
    usuarios = models.Usuario.objects.all()
    total = usuarios.count()
    return render(request, 'usuario-home.html', {
        'Usuarios': usuarios,
        'Total': total,
        'titlePage': 'Listado Usuarios'
    })


def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('users:detalle_usuario', id_usuario=usuario.id)
    else:
        form = UsuarioForm()
    return render(request, 'usuario-detail.html', {
        'form': form,
        'titulo': 'Crear usuario',
        'boton_text': 'Crear',
        'titlePage': 'Crear usuario'
    })


def detalle_usuario(request, id_usuario):
    usuario = models.Usuario.objects.get(pk=id_usuario)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario se ha actualizado correctamente.')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario-detail.html', {
        'form': form,
        'usuario': usuario,
        'titulo': 'Editar usuario',
        'boton_text': 'Actualizar',
        'titlePage': 'Editar usuario'
    })


def buscar_usuario(request):
    return render(request, 'usuario-search.html', {
        'titlePage': 'Filtrar búsqueda'
    })


def filtrar_usuarios(request):
    usuarios = models.Usuario.objects.all()
    nombre = request.GET.get('nombre', '').strip()
    documento = request.GET.get('documento', '').strip()
    rol = request.GET.get('rol', '')
    if nombre:
        usuarios = usuarios.filter(nombre__icontains=nombre) | usuarios.filter(apellido__icontains=nombre)
    if documento:
        usuarios = usuarios.filter(numero_documento__icontains=documento)
    if rol:
        usuarios = usuarios.filter(rol_id=rol)
    total = usuarios.count()
    return render(request, 'usuario-home.html', {
        'Usuarios': usuarios,
        'Total': total,
        'titulo': 'Resultados de búsqueda'
    })


def eliminar_usuario(request, id_usuario):
    try:
        usuario = models.Usuario.objects.get(pk=id_usuario)
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    except models.Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe o ya fue eliminado.')
    return redirect('users:listado_usuarios')


def home_cuentas(request):
    cuentas = models.Cuenta_Usuario.objects.all()
    total = cuentas.count()
    return render(request, 'cuenta-home.html', {
        'Cuentas': cuentas,
        'Total': total,
        'titlePage': 'Listado Cuentas'
    })


def crear_cuenta(request):
    if request.method == "POST":
        form = CuentaUsuarioForm(request.POST)
        if form.is_valid():
            cuenta = form.save()
            messages.success(request, 'Cuenta de usuario creada correctamente.')
            return redirect('users:editar_cuenta', id_cuenta=cuenta.id)
    else:
        form = CuentaUsuarioForm()
    return render(request, 'cuenta-detail.html', {
        'form': form,
        'titulo': 'Crear cuenta',
        'boton_text': 'Crear',
        'titlePage': 'Crear cuenta'
    })


def editar_cuenta(request, id_cuenta):
    cuenta = models.Cuenta_Usuario.objects.get(pk=id_cuenta)
    if request.method == "POST":
        form = CuentaUsuarioForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, 'La cuenta se ha actualizado correctamente.')
    else:
        form = CuentaUsuarioForm(instance=cuenta)
    return render(request, 'cuenta-detail.html', {
        'form': form,
        'cuenta': cuenta,
        'titulo': 'Editar cuenta',
        'boton_text': 'Actualizar',
        'titlePage': 'Editar cuenta'
    })


def _generar_pdf(html_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    response.write(result_file.getvalue())
    return response


def generar_pdf_factura(request, id_factura):
    from Aplicaciones.billing import models as billing_models
    factura = billing_models.Factura.objects.get(id=id_factura)
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    servicio_total = factura.servicio_precio * factura.servicio_cantidad
    html_content = render(request, 'pdf_factura.html', {
        'factura': factura,
        'fecha': fecha,
        'servicio_total': servicio_total,
    }).content.decode('utf-8')
    return _generar_pdf(html_content, f'factura_{factura.id}.pdf')
