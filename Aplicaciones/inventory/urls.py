from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path('categoria/', views.home_categorias, name='listado_categorias'),
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:id_categoria>/', views.editar_categoria, name='editar_categoria'),
    path('proveedor/', views.home_proveedores, name='listado_proveedores'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/<int:id_proveedor>/', views.editar_proveedor, name='editar_proveedor'),
    path('', views.home_producto, name='listado_productos'),
    path('<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('filtrar/', views.filtrar_productos, name='filtrar_productos'),
    path('eliminado/<int:id_producto>', views.eliminar_producto, name='eliminar_producto')
]
