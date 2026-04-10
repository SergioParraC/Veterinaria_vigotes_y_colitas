from django.shortcuts import render, redirect
from . import models

'''Listado de categorias'''
def home_categorias(request):
    categorias = models.Categoria.objects.all()
    return render(request, 'categoria-home.html', {
        'Categorias': categorias
    })

'''Crear una nueva categoria'''
def crear_categoria(request):
    categoria_vacia = models.Categoria(nombre='', descripcion='')
    if request.method == "POST":
        data = request.POST
        categoria = models.Categoria()
        categoria.nombre = data.get("Nombre")
        categoria.descripcion = data.get("Descripcion")
        categoria.save()
        return redirect('editar_categoria', id_categoria=categoria.id)
    return render(request, 'categoria-detail.html', {
        'categoria': categoria_vacia,
        'titulo': 'Crear categoría',
        'boton': 'Crear'
    })

'''Editar categoria, usando el mismo template para crear'''
def editar_categoria(request, id_categoria):
    categoria = models.Categoria.objects.get(pk=id_categoria)
    if request.method == "POST":
        data = request.POST
        categoria.nombre = data.get("Nombre")
        categoria.descripcion = data.get("Descripcion")
        categoria.save()
        return render(request, 'categoria-detail.html', {
            'categoria': categoria,
            'titulo': 'Editar categoría',
            'boton': 'Actualizar',
            'mensaje': 'Categoría actualizada correctamente.'
        })
    return render(request, 'categoria-detail.html', {
        'categoria': categoria,
        'titulo': 'Editar categoría',
        'boton': 'Actualizar'
    })

'''Listado de proveedores'''
def home_proveedores(request):
    proveedores = models.Proveedor.objects.all()
    total = proveedores.count()
    return render(request, 'proveedor-home.html', {
        'Proveedores': proveedores,
        'Total': total
    })

'''Crear un nuevo proveedor'''
def crear_proveedor(request):
    proveedor_vacio = models.Proveedor(nombre='', contacto='', telefono='', email='', direccion='')
    if request.method == "POST":
        data = request.POST
        proveedor = models.Proveedor()
        proveedor.nombre = data.get("Nombre")
        proveedor.contacto = data.get("Contacto")
        proveedor.telefono = data.get("Telefono")
        proveedor.email = data.get("Email")
        proveedor.direccion = data.get("Direccion")
        proveedor.save()
        return redirect('editar_proveedor', id_proveedor=proveedor.id)
    return render(request, 'proveedor-detail.html', {
        'proveedor': proveedor_vacio,
        'titulo': 'Crear proveedor',
        'boton_text': 'Crear'
    })

'''Editar proveedor, usando el mismo template para crear'''
def editar_proveedor(request, id_proveedor):
    proveedor = models.Proveedor.objects.get(pk=id_proveedor)
    if request.method == "POST":
        data = request.POST
        proveedor.nombre = data.get("Nombre")
        proveedor.contacto = data.get("Contacto")
        proveedor.telefono = data.get("Telefono")
        proveedor.email = data.get("Email")
        proveedor.direccion = data.get("Direccion")
        proveedor.save()
        return render(request, 'proveedor-detail.html', {
            'proveedor': proveedor,
            'titulo': 'Editar proveedor',
            'boton_text': 'Actualizar',
            'mensaje': "El proveedor se ha actualizado correctamente"
        })
    return render(request, 'proveedor-detail.html', {
        'proveedor': proveedor,
        'titulo': 'Editar proveedor',
        'boton_text': 'Actualizar'
    })

'''Listado de productos'''
def home_producto(request):
    dataProductos = models.Producto.objects.all()
    dataTotal = models.Producto.objects.count()
    data = {
        'Productos': dataProductos,
        'Total': dataTotal,
        'titulo': "Todos los productos"
    }
    return render(request, 'inventory-home.html', data)

'''Crear un producto'''
def crear_producto(request):
    categorias = models.Categoria.objects.all()
    proveedores = models.Proveedor.objects.all()
    producto_vacio = models.Producto(
        nombre='',
        categoria=None,
        proveedor=None,
        descripcion='',
        precio='',
        stock='',
        img=None
    )
    data = {
        'producto': producto_vacio,
        'categorias': categorias,
        'proveedores': proveedores,
        'boton': "Crear",
        'titulo': "Crear producto"
    }
    if request.method == "POST":
        data_post = request.POST
        files = request.FILES
        producto = models.Producto()
        producto.nombre = data_post.get("Nombre")
        producto.categoria_id = data_post.get("Categoria")
        producto.proveedor_id = data_post.get("Proveedor")
        producto.descripcion = data_post.get("Descripcion")
        producto.precio = data_post.get("Precio")
        producto.stock = data_post.get("Stock")
        producto.img = files.get("Imagen")
        producto.save()
        return redirect('detalle_producto', id_producto=producto.id)
    return render(request, 'inventory-detail.html', data)

'''Detalles de cada producto para crear uno nuevo'''
def detalle_producto(request, id_producto):
    dataProducto = models.Producto.objects.get(pk = id_producto)
    categorias = models.Categoria.objects.all()
    proveedores = models.Proveedor.objects.all()
    data = { 'producto' : dataProducto,
             'categorias' : categorias,
             'proveedores' : proveedores,
             'boton' : "Actualizar",
             'titulo' : "Editar producto"
             }
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        producto = dataProducto
        producto.nombre = data.get("Nombre")
        producto.categoria_id = data.get("Categoria")
        producto.proveedor_id = data.get("Proveedor")
        producto.descripcion = data.get("Descripcion")
        producto.precio = data.get("Precio")
        producto.stock = data.get("Stock")
        if files.get("Imagen"):
            producto.img = files.get("Imagen")
        producto.save()
        return render(request, 'inventory-detail.html', {
            'producto': producto,
            'categorias': categorias,
            'proveedores': proveedores,
            'mensaje': "Producto editado exitosamente",
            'boton': "Actualizar"
        })
    return render(request, 'inventory-detail.html', data)

'''Vista para buscar productos'''
def buscar_producto(request):
    categorias = models.Categoria.objects.all()
    return render(request, 'inventory-search.html', {'categorias': categorias})

'''Se pasan los filtros por GET, se filtran los productos'''
def filtrar_productos(request):
    productos = models.Producto.objects.all()
    nombre = request.GET.get('nombre', '').strip()
    categoria = request.GET.get('categoria', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    dataTotal = productos.count()
    return render(request, 'inventory-home.html', {
        'Productos': productos,
        'Total': dataTotal,
        'titulo': "Resultados de búsqueda"
    })