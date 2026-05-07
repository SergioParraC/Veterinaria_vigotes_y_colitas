from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from . import forms
from Aplicaciones.billing import models as billing_models


# Se dejan comentarios en productos, ya que es la base para el resto de elementos


'''Listado de categorias'''
def home_categorias(request):
    categorias = models.Categoria.objects.all()
    data = {
        'Categorias': categorias,
        'titlePage': "Crear categoría"
    }
    return render(request, 'categoria-home.html', data)

'''Crear una nueva categoria'''
def crear_categoria_formulario(request):
    if request.method == "POST":
        formulario = forms.CategoriaForm(request.POST)
        if formulario.is_valid():
            categoria = models.Categoria()
            categoria.nombre = formulario.cleaned_data["nombre"]
            categoria.descripcion = formulario.cleaned_data["descripcion"]
            categoria.save()
        categoria.nombre = data.get("Nombre")
        categoria.descripcion = data.get("Descripcion")
        categoria.save()
        return redirect('inventario:editar_categoria', id_categoria=categoria.id)
    else:
        formulario = forms.CategoriaForm()
    data = {
        'formulario': formulario,
        'titulo': 'Crear categoría',
        'boton': 'Crear',
        'titlePage': 'Crear categoría'
    }
    return render(request, 'categoria-detail.html', data)

'''Editar categoria, usando el mismo template para crear'''
def guardar_categoria(request, id_categoria):
    categoria = models.Categoria.objects.get(pk=id_categoria)
    if request.method == "POST":
        formulario = forms.CategoriaForm(request.POST)
        if formulario.is_valid():
            categoria.nombre = formulario.cleaned_data["nombre"]
            categoria.descripcion = formulario.cleaned_data["descripcion"]
            categoria.save()

            data = {
                'categoria': categoria,
                'formulario': forms.CategoriaForm(initial={
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion
                }),
                'titulo': 'Editar categoría',
                'boton': 'Actualizar',
                'mensaje': 'Categoría actualizada correctamente.',
                'titlePage': 'Editar Categoría'
            }
            return render(request, 'categoria-detail.html', data)
        data = {
            'categoria': categoria,
            'formulario': formulario,
            'titulo': 'Editar categoría',
            'boton': 'Actualizar',
            'titlePage': 'Editar Categoría',
            'mensaje': formulario.errors.as_text()
        }
        return render(request, 'categoria-detail.html', data)
    else:
        formulario = forms.CategoriaForm(initial={
            'nombre': categoria.nombre,
            'descripcion': categoria.descripcion
        })
        data = {
            'categoria': categoria,
            'formulario': formulario,
            'titulo': 'Editar categoría',
            'boton': 'Actualizar',
            'titlePage': 'Editar Categoría'
        }
    return render(request, 'categoria-detail.html', data)

'''Listado de proveedores'''
def home_proveedores(request):
    proveedores = models.Proveedor.objects.all()
    total = proveedores.count()
    return render(request, 'proveedor-home.html', {
        'proveedores': proveedores,
        'total': total,
        'titlePage': 'Listado Proveedores'
    })

'''Crear un nuevo proveedor'''
def crear_proveedor_formulario(request):
    if request.method == "POST":
        formulario = forms.ProveedorForm(request.POST)
        if formulario.is_valid():
            proveedor = models.Proveedor()
            proveedor.nombre = formulario.cleaned_data["nombre"]
            proveedor.contacto = formulario.cleaned_data["contacto"]
            proveedor.telefono = formulario.cleaned_data["telefono"]
            proveedor.email = formulario.cleaned_data["email"]
            proveedor.direccion = formulario.cleaned_data["direccion"]
            proveedor.save()
            mensaje = 'Proveedor creado correctamente.'
        return redirect('inventario:editar_proveedor', id_proveedor=proveedor.id)
    else:
        formulario = forms.ProveedorForm()
    data = {
        'formulario': formulario,
        'titulo': 'Crear proveedor',
        'boton_text': 'Crear',
        'titlePage': 'Crear proveedor'
    }
    return render(request, 'proveedor-detail.html', data)

'''Eliminar un proveedor por ID'''
def eliminar_proveedor(request, id_proveedor):
    try:
        proveedor = models.Proveedor.objects.get(pk=id_proveedor)
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
    except models.Proveedor.DoesNotExist:
        messages.error(request, 'El proveedor no existe o ya fue eliminado.')
    return redirect('inventario:listado_proveedores')

'''Editar proveedor, usando el mismo template para crear'''
def guardar_proveedor(request, id_proveedor):
    proveedor = models.Proveedor.objects.get(pk=id_proveedor)
    if request.method == "POST":
        formulario = forms.ProveedorForm(request.POST)
        if formulario.is_valid():
            proveedor.nombre = formulario.cleaned_data["nombre"]
            proveedor.contacto = formulario.cleaned_data["contacto"]
            proveedor.telefono = formulario.cleaned_data["telefono"]
            proveedor.email = formulario.cleaned_data["email"]
            proveedor.direccion = formulario.cleaned_data["direccion"]
            proveedor.save()
            data = {
                'proveedor': proveedor,
                'formulario': forms.ProveedorForm(initial={
                    'nombre': proveedor.nombre,
                    'contacto': proveedor.contacto,
                    'telefono': proveedor.telefono,
                    'email': proveedor.email,
                    'direccion': proveedor.direccion
                }),
                'titulo': 'Editar proveedor',
                'boton_text': 'Actualizar',
                'mensaje': 'El proveedor se ha actualizado correctamente',
                'titlePage': 'Editar proveedor'
            }
            return render(request, 'proveedor-detail.html', data)
        data = {
            'formulario': formulario,
            'proveedor': proveedor,
            'titulo': 'Editar proveedor',
            'boton_text': 'Actualizar',
            'titlePage': 'Editar proveedor',
            'mensaje': formulario.errors.as_text()
        }
        return render(request, 'proveedor-detail.html', data)
    else:
        formulario = forms.ProveedorForm(initial={
            'nombre': proveedor.nombre,
            'contacto': proveedor.contacto,
            'telefono': proveedor.telefono,
            'email': proveedor.email,
            'direccion': proveedor.direccion
        })
        data = {
            'formulario': formulario,
            'proveedor': proveedor,
            'titulo': 'Editar proveedor',
            'boton_text': 'Actualizar',
            'titlePage': 'Editar proveedor'
        }
    return render(request, 'proveedor-detail.html', data)

'''Listado de productos'''
def home_producto(request):
    # Trae todos los productos, y un totalizador
    dataProductos = models.Producto.objects.all()
    dataTotal = models.Producto.objects.count()
    # Se envia el formulario de filtro
    data = {
        'formulario': forms.BuscarProductosForm(),
        'Productos': dataProductos,
        'Total': dataTotal,
        'titulo': 'Todos los productos',
        'titlePage': 'Productos'
    }
    return render(request, 'inventory-home.html', data)


def productos_cliente(request):
    carrito_compras = billing_models.Factura.objects.filter(estado='BORRADOR').first()
    cant_elementos_carrito = 0
    if carrito_compras:
        cant_elementos_carrito = billing_models.FacturaDetalle.objects.filter(factura=carrito_compras).count()
    productos = models.Producto.objects.all()
    total = productos.count()
    data = {
        'formulario': forms.BuscarProductosForm(),
        'Productos': productos,
        'Total': total,
        'titulo': 'Catalogo de productos',
        'titlePage': 'Catalogo cliente',
        'cant_elementos_carrito': cant_elementos_carrito
    }
    return render(request, 'productos_cliente.html', data)


def detalle_producto_cliente(request, id_producto):
    carrito_compras = billing_models.Factura.objects.filter(estado='BORRADOR').first()
    cant_elementos_carrito = 0
    if carrito_compras:
        cant_elementos_carrito = billing_models.FacturaDetalle.objects.filter(factura=carrito_compras).count()
    producto = models.Producto.objects.get(pk=id_producto)
    data = {
        'producto': producto,
        'titulo': producto.nombre,
        'titlePage': f'Detalle | {producto.nombre}',
        'cant_elementos_carrito': cant_elementos_carrito
    }
    return render(request, 'productos-cliente-detail.html', data)

'''Crear un producto'''
def crear_producto_formulario(request):
    # Validación de formulario por PST
    if request.method == "POST":
        formulario = forms.ProductForm(request.POST, request.FILES)
        # Si el formulario es válido, se crea un nuevo producto con los datos del formulario y se guarda en la base de datos
        if formulario.is_valid():
            producto = models.Producto()
            producto.nombre = formulario.cleaned_data["nombre"]
            producto.categoria = formulario.cleaned_data["categoria"]
            producto.proveedor = formulario.cleaned_data["proveedor"]
            producto.descripcion = formulario.cleaned_data["descripcion"]
            producto.precio = formulario.cleaned_data["precio"]
            producto.stock = formulario.cleaned_data["cantidad_en_stock"]
            # Imagen es opcional
            if formulario.cleaned_data.get("imagen"):
                producto.img = formulario.cleaned_data["imagen"]
            producto.save()
            # Redirige a la pagina de edicion, por el ID
            return redirect('inventario:guardar_producto', id_producto=producto.id)
    else:
        formulario = forms.ProductForm()

    data = {
        'formulario': formulario,
        'producto': None,
        'boton': 'Crear',
        'titulo': 'Crear producto',
        'titlePage': 'Crear producto',
    }
    return render(request, 'inventory-detail.html', data)

'''Detalles de cada producto para crear uno nuevo'''
def guardar_producto(request, id_producto):
    # Se trae el producto por ID
    producto = models.Producto.objects.get(pk = id_producto)
    # Si se envia el formulario por POST, se valida y se actualiza el producto
    if request.method == "POST":
        formulario = forms.ProductForm(request.POST, request.FILES)
        if formulario.is_valid():
            producto.nombre = formulario.cleaned_data["nombre"]
            producto.categoria = formulario.cleaned_data["categoria"]
            producto.proveedor = formulario.cleaned_data["proveedor"]
            producto.descripcion = formulario.cleaned_data["descripcion"]
            producto.precio = formulario.cleaned_data["precio"]
            producto.stock = formulario.cleaned_data["cantidad_en_stock"]
            if formulario.cleaned_data.get("imagen"):
                producto.img = formulario.cleaned_data["imagen"]
            producto.save()
            data = {
                'producto' : producto,
                'formulario': forms.ProductForm(initial={
                    'nombre': producto.nombre,
                    'categoria': producto.categoria_id,
                    'proveedor': producto.proveedor_id,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'cantidad_en_stock': producto.stock
                }),
                'boton' : 'Actualizar',
                'titulo' : 'Editar producto',
                'mensaje': 'Producto actualizado correctamente.',
                'titlePage': 'Editar producto'
             }
            return render(request, 'inventory-detail.html', data)
        # Si no es válido, se muestra el formulario con datos iniciales y con los errores
        data = {
            'producto': producto,
            'formulario': formulario,
            'boton': 'Actualizar',
            'titulo': 'Editar producto',
            'titlePage': 'Editar producto',
            'mensaje': formulario.errors.as_text()
        }
        return render(request, 'inventory-detail.html', data)
    # Si es otro método, se muestra el formulario con los datos del producto
    else: 
        # Se carga el formulario con los datos del producto para mostrar en el template
        formulario = forms.ProductForm(initial={
            'nombre': producto.nombre,
            'categoria': producto.categoria_id,
            'proveedor': producto.proveedor_id,
            'descripcion': producto.descripcion,
            'precio': producto.precio,
            'cantidad_en_stock': producto.stock
        })
        # Se envia el producto para el id y el formulario
        data = {
            'producto': producto,
            'formulario': formulario,
            'boton': 'Actualizar',
            'titulo': 'Editar producto',
            'titlePage': 'Editar producto'
        }
    # Se renderiza el formuario según la data armada
    return render(request, 'inventory-detail.html', data)

'''Se pasan los filtros por POST, se filtran los productos'''
def filtrar_productos(request):
    # Se obtiene el formulario con los datos enviados por POST
    formulario = forms.BuscarProductosForm(request.POST)
    # Se obtienen todos los productos para luego aplicar los filtros
    productos = models.Producto.objects.all()
    # Se obtienen los datos del formulario para aplicar los filtros correspondientes
    nombre = formulario.data.get('nombre', '')
    categoria = formulario.data.get('categoria', '')
    precio_min = formulario.data.get('precio_minimo', '')
    precio_max = formulario.data.get('precio_maximo', '')
    # Cada filtro no es obligatorio, se verifica
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    dataTotal = productos.count()
    data = {
        'formulario': formulario,
        'Productos': productos,
        'Total': dataTotal,
        'titulo': 'Resultados de búsqueda',
        'titlePage': 'Resultados de búsqueda',
        'volver_menu': True
    }
    return render(request, 'inventory-home.html', data)

'''Eliminar un producto por ID'''
def eliminar_producto(request, id_producto):
    try:
        # Obtiene el producto por su ID y lo elimina
        producto = models.Producto.objects.get(pk=id_producto)
        producto.delete()
        # Manera de enviar mensajes de éxito o error al template usando el framework de mensajes de Django
        messages.success(request, 'Producto eliminado exitosamente.')
    except models.Producto.DoesNotExist:
        messages.error(request, 'El producto no existe o ya fue eliminado.')
    return redirect('inventario:listado_productos')


def _generar_pdf(html_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    response.write(result_file.getvalue())
    return response


def generar_pdf_productos(request):
    productos = models.Producto.objects.all()
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    filas = ''
    for p in productos:
        stock_style = 'font-weight: bold; color: #d32f2f;' if p.stock <= 10 else ''
        filas += f'''
        <tr>
            <td>{p.nombre}</td>
            <td>{p.categoria}</td>
            <td>{p.proveedor}</td>
            <td>{p.descripcion or ''}</td>
            <td>$ {p.precio}</td>
            <td style="{stock_style}">{p.stock}</td>
        </tr>'''
    html = f'''
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Helvetica, sans-serif; font-size: 12px; }}
            h1 {{ color: #146105; text-align: center; }}
            .fecha {{ text-align: right; font-size: 10px; color: #666; margin-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #acffaf; color: #000; padding: 6px 8px; border: 1px solid #000; text-align: left; }}
            td {{ padding: 5px 8px; border: 1px solid #000; }}
            .total {{ margin-top: 10px; font-size: 14px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Listado de Productos</h1>
        <p class="fecha">Generado: {fecha}</p>
        <table>
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Categoria</th>
                    <th>Proveedor</th>
                    <th>Descripcion</th>
                    <th>Precio</th>
                    <th>Stock</th>
                </tr>
            </thead>
            <tbody>{filas}</tbody>
        </table>
        <p class="total">Total de productos: {productos.count()}</p>
    </body>
    </html>'''
    return _generar_pdf(html, 'productos.pdf')


def generar_pdf_proveedores(request):
    proveedores = models.Proveedor.objects.all()
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    filas = ''
    for p in proveedores:
        filas += f'''
        <tr>
            <td>{p.nombre}</td>
            <td>{p.contacto}</td>
            <td>{p.telefono}</td>
            <td>{p.email}</td>
            <td>{p.direccion}</td>
        </tr>'''
    html = f'''
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Helvetica, sans-serif; font-size: 12px; }}
            h1 {{ color: #146105; text-align: center; }}
            .fecha {{ text-align: right; font-size: 10px; color: #666; margin-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #acffaf; color: #000; padding: 6px 8px; border: 1px solid #000; text-align: left; }}
            td {{ padding: 5px 8px; border: 1px solid #000; }}
            .total {{ margin-top: 10px; font-size: 14px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Listado de Proveedores</h1>
        <p class="fecha">Generado: {fecha}</p>
        <table>
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Contacto</th>
                    <th>Telefono</th>
                    <th>Email</th>
                    <th>Direccion</th>
                </tr>
            </thead>
            <tbody>{filas}</tbody>
        </table>
        <p class="total">Total de proveedores: {proveedores.count()}</p>
    </body>
    </html>'''
    return _generar_pdf(html, 'proveedores.pdf')