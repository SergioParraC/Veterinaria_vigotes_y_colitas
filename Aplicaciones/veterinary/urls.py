from django.urls import path
from . import views
from Aplicaciones.users.views import generar_pdf_factura

app_name = "citas"

urlpatterns = [
    path('', views.home_citas, name='listado_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('<int:id_cita>/', views.detalle_cita, name='detalle_cita'),
    path('buscar/', views.buscar_cita, name='buscar_cita'),
    path('filtrar/', views.filtrar_citas, name='filtrar_citas'),
    path('eliminado/<int:id_cita>', views.eliminar_cita, name='eliminar_cita'),
    path('factura/<int:id_factura>/pdf/', generar_pdf_factura, name='pdf_factura'),
]