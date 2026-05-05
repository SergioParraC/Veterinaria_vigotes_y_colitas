from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Aplicaciones.home.urls')),
    path('inventario/', include(('Aplicaciones.inventory.urls', 'inventario'), namespace='inventario')),
    path('inventario/carrito/', include(('Aplicaciones.billing.urls', 'billing'), namespace='billing_invetario')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)