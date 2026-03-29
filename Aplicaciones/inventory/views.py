from django.shortcuts import render
from . import models

def home(request):
    dataProductos = models.Producto.objects.all()
    dataTotal = models.Producto.objects.count
    data = {
        'Productos': dataProductos,
        'Total': dataTotal
    }
    return render(request, 'inventory-home.html', data)

def detalle(request, id_producto):
    dataProducto = models.Producto.objects.get(pk = id_producto)
    data = { 'producto' : dataProducto }
    return render(request, 'inventory-detail.html', data)
