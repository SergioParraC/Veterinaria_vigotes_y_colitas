from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Aplicaciones.home.urls')),
    path('inventario/', include('Aplicaciones.inventory.urls'))
]
