from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_pets),
    path('mascotas/<int:id_mascota>/historia/', views.historia_mascota),
    path('mascotas/crear/', views.registrar_mascota),
    path('citas/crear/', views.registrar_cita),
    path('vacunas/crear/', views.registrar_vacuna),
    path('historiales/crear/', views.registrar_historial),
]
