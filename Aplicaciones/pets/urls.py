from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_pets),
    path('mascotas/<int:id_mascota>/historia/', views.historia_mascota),
    path('mascotas/crear/', views.registrar_mascota),
    path('mascotas/<int:id_mascota>/editar/', views.editar_mascota),
    path('vacunas/crear/', views.registrar_vacuna),
    path('vacunas/<int:id_vacuna>/editar/', views.editar_vacuna),
    path('historiales/crear/', views.registrar_historial),
    path('historiales/<int:id_historial>/editar/', views.editar_historial),
]
