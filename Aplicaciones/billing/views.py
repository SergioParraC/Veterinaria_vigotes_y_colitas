from django.shortcuts import render, redirect
from . import models
from . import forms
from Aplicaciones.inventory.models import Producto
from decimal import Decimal

from django.http import HttpResponse
from datetime import datetime
'''Necesario para PDF'''
from io import BytesIO
from xhtml2pdf import pisa

from django.utils import timezone
'''Vistas para el proceso de facturación, incluyendo selección de cliente, selección de mascota, añadir productos al carrito y mostrar el carrito de compras.'''

'''Crea elemento nuevo del inventario'''
def anadirItemInventario(request, id_producto):
    # Trae el producto seleccionado para añadir al carrito
    producto = Producto.objects.get(id=id_producto)
    if request.method == 'POST':
        # Obitiene la cantidad
        cantidad = int(request.POST.get('cantidad', 1))
        # Buscar si hay una factura en modo borrador
        facturaActual = models.Factura.objects.filter(estado='BORRADOR').first()
        try:
            #si no hay factura en modo borrador, redirige a seleccionar cliente para crear una nueva factura
            if not facturaActual:
                # Métodos en donde se guardan elementos en sesión, y se usarán más adelante despues de seleccionar cliente y mascota
                request.session['id_producto'] = id_producto
                request.session['cantidad'] = cantidad
                return redirect('billing:seleccionar_cliente')
            else:
                # Ya hay una factura en modo borrador, se añade el producto seleccionado a esa factura
                cantidad = int(request.POST.get('cantidad', 1))
                nuevoDetalle = models.FacturaDetalle(
                    factura=facturaActual,
                    tipo='PRODUCTO',
                    producto=producto,
                    descripcion=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    subtotal=producto.precio * cantidad
                )
                nuevoDetalle.save()
                # Disminuye la cantidad de lementos para el producto en cuestion
                producto.stock -= cantidad
                producto.save()
                # Valida si se añadio desde la pag principal o desde detalles, y redirige
                return redirect('inventario:productos_cliente')
        # Si ocurre un error, redirige
        except Exception as e:
            return redirect('inventario:productos_cliente')
    return render(request, 'añadir_item_inventario.html')

'''Vista para seleccionar el cliente'''
def seleccionar_cliente(request):
    if request.method == 'POST':
        # Resderiza el formulario para seleccionar primero el cliente
        formulario = forms.CrearFacturaClienteForm(request.POST)
        if formulario.is_valid():
            # Obtiene el cliente seleccionado
            clienteSeleccionado = formulario.cleaned_data['cliente']
            # Guarda el cliente seleccionado en la sesión para usarlo más adelante en el proceso de facturación
            request.session['cliente_id'] = clienteSeleccionado.id
            return redirect('billing:seleccionar_mascota')
        return render(request, 'seleccionar_cliente.html', {'formulario': formulario})
    return render(request, 'seleccionar_cliente.html', {'formulario': forms.CrearFacturaClienteForm()})

'''Vista para seleccionar la mascota, después de seleccionar el cliente'''
# NOTA: Ver formulario para entender la lógica de mostrar solo las mascotas del cliente seleccionado
def seleccionar_mascota(request):
    # Obtiene los datos guardados en la sesión
    cliente_id = request.session.get('cliente_id')
    id_producto = request.session.get('id_producto')
    # Trae el producto seleccionado para añadir al carrito
    producto = Producto.objects.get(id=id_producto)
    if request.method == 'POST':
        # Trae la respuesta del formulario
        formulario = forms.CrearFacturaMascotaForm(request.POST, cliente_id=cliente_id)
        if formulario.is_valid():
            # Trae la mascota seleccionada, y si no se seleccionó ninguna, se asigna None para evitar errores
            mascota = formulario.cleaned_data['mascota']
            mascota_id = mascota.id if mascota else None
            # Crea la factura en estado BORRADOR
            factura = models.Factura.objects.create(
                cliente_id=cliente_id,
                mascota_id=mascota_id,
                fecha=timezone.now(),
                estado='BORRADOR'
            )
            # Obtiene la cantidad desde la sesión, si no hay cantidad, se asigna 1 por defecto
            cantidad = request.session.get('cantidad', 1)
            # Crea el detalle de la factura con el producto seleccionado y la cantidad
            models.FacturaDetalle.objects.create(
                factura=factura,
                tipo='PRODUCTO',
                producto=producto,
                descripcion=producto.nombre,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=producto.precio * int(cantidad)
            )
            # Disminuye la cantidad de elementos para el producto en cuestion
            producto.stock -= int(cantidad)
            producto.save()
            # Redirige despendiendo de la pag de origen
            return redirect('inventario:productos_cliente')

        # Si el formulario no es válido, vuelve a mostrarlo con errores
        return render(request, 'seleccionar_mascota.html', {'formulario': formulario})
    else:
        # Cuando el método es GET, se muestra el formulario para seleccionar la mascota, filtrando solo las mascotas del cliente seleccionado
        formulario = forms.CrearFacturaMascotaForm(cliente_id=cliente_id)
        return render(request, 'seleccionar_mascota.html', {'formulario': formulario})
    
'''Muestra todos los elementos que se encuentran en el carrito'''
def mostrar_carrito(request):
    # Filtra si hay una factura en estado BORRADOR, si no hay ninguna, se envia un carrito vacio
    factura = models.Factura.objects.filter(estado='BORRADOR').first()
    if not factura:
        # Se valida en vista cuando no hay ningún elementos en el carrito
        return render(request, 'mostrar_carrito.html', {'detalles': [], 'total': 0})
    detalles = models.FacturaDetalle.objects.filter(factura=factura)
    total = sum(detalle.subtotal for detalle in detalles)
    return render(request, 'mostrar_carrito.html', {'detalles': detalles, 'total': total})

'''Cambia el estado de la compra a PAGADA, y calcula el total de la factura'''
def finalizar_compra(request):
    factura = models.Factura.objects.filter(estado='BORRADOR').first()
    if factura:
        detalles = models.FacturaDetalle.objects.filter(factura=factura)
        total = sum(detalle.subtotal for detalle in detalles)
        factura.subtotal = total * Decimal(0.81)  #Subtotal sin IVA
        factura.iva = total * Decimal(0.19)  #IVA del 19%
        factura.total = total + factura.iva
        factura.estado = 'PAGADA'
        factura.save()
    return redirect('billing:listar_facturas')

'''Muestra el listado de todas las facturas creadas'''
def listar_facturas(request):
    facturas = models.Factura.objects.all()
    return render(request, 'listado_facturas.html', {'facturas': facturas})

'''Genera un PDF con los detalles de la factura'''
def _generar_pdf(html_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    response.write(result_file.getvalue())
    return response

'''Vista que renderiza el PDF de la factura seleccionada'''
def generar_pdf_factura(request, id_factura):
    # Trae la factura y sus detalles para renderizarlos en el PDF
    factura = models.Factura.objects.get(id=id_factura)
    detalles = models.FacturaDetalle.objects.filter(factura=factura)
    #Envia datos de la factura y la plantilla HTML para renderizar la información
    html_content = render(request, 'pdf_factura.html', {'factura': factura, 'detalles': detalles}).content.decode('utf-8')
    filename = f'factura_{factura.id}.pdf'
    return _generar_pdf(html_content, filename)
