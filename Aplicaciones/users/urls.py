from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('perfil/', views.home_perfiles, name='listado_perfiles'),
    path('perfil/crear/', views.crear_perfil, name='crear_perfil'),
    path('perfil/<int:id_perfil>/', views.editar_perfil, name='editar_perfil'),
    path('usuario/', views.home_usuarios, name='listado_usuarios'),
    path('usuario/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuario/<int:id_usuario>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/buscar/', views.buscar_usuario, name='buscar_usuario'),
    path('usuario/filtrar/', views.filtrar_usuarios, name='filtrar_usuarios'),
    path('usuario/eliminado/<int:id_usuario>', views.eliminar_usuario, name='eliminar_usuario'),
    path('cuenta/', views.home_cuentas, name='listado_cuentas'),
    path('cuenta/crear/', views.crear_cuenta, name='crear_cuenta'),
    path('cuenta/<int:id_cuenta>/', views.editar_cuenta, name='editar_cuenta'),
    path('factura/<int:id_factura>/pdf/', views.generar_pdf_factura, name='pdf_factura'),
]
