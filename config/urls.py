from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Aplicaciones.home.urls')),
    path('inventario/', include(('Aplicaciones.inventory.urls', 'inventario'), namespace='inventario')),
    path('citas/', include(('Aplicaciones.veterinary.urls', 'citas'), namespace='citas')),
    path('users/', include(('Aplicaciones.users.urls', 'users'), namespace='users')),
    path('veterinary/', RedirectView.as_view(url='/citas/', permanent=False)),
    re_path(r'^veterinary/(?P<path>.*)$', RedirectView.as_view(url='/citas/%(path)s', permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)