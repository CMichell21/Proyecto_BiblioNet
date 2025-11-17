from django.contrib import admin
from django.urls import path, include
from seguridad import views as seguridad_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Alias para que los tests encuentren estos nombres 
    path("login/", seguridad_views.iniciar_sesion_empleado, name="login-page"),
    path("logout/", seguridad_views.cerrar_sesion_empleado, name="logout-page"),
    path("mi-cuenta/", seguridad_views.panel_administrador, name="mi-cuenta"),

    path("", include("biblio.urls")),      # Inicio, catálogo, login cliente…
    path("", include("seguridad.urls")),   # Login empleados y panel admin
]


