from django.urls import path
from . import views

urlpatterns = [
    # --- RUTAS PÚBLICAS ---
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    
    # Nota: He quitado la duplicación de 'acerca_de' y añadido un prefijo 'publico/' 
    # para evitar conflictos si tienes otras URLs de admin/empleado.
    path("acerca-de/", views.acerca_de, name="acerca_de"),
    path("registro/", views.registro_cliente, name="registro_cliente"),
    path("clientes/inicio_sesion/", views.inicio_sesion_cliente, name="inicio_sesion_cliente"),
    
    # --- RUTAS DE CLIENTES PROTEGIDAS (Requieren Sesión) ---
    path('clientes/pantalla_inicio/', views.pantalla_inicio_cliente, name='pantalla_inicio_cliente'),
    path('clientes/catalogo_cliente/', views.catalogo_cliente, name='catalogo_cliente'),
    path('clientes/cerrar_sesion/', views.cerrar_sesion_cliente, name='cerrar_sesion_cliente'),
    
    # --- FUNCIONALIDAD DE RESERVAS ---
    
    # 1. MUESTRA LA PÁGINA DE CONFIRMACIÓN (GET - Llamado desde catalogo_cliente.html)
    # RUTA: /clientes/reservar/confirmar/5/
    path("clientes/reservar/confirmar/<int:libro_id>/", views.confirmar_reserva, name="confirmar_reserva"),
    
    # 2. PROCESA LA CREACIÓN DE LA RESERVA (POST - Llamado desde confirmar_reserva.html)
    # RUTA: /clientes/reservar/crear/5/
    path('clientes/reservar/crear/<int:libro_id>/', views.reservar_libro, name='crear_reserva'),
    
    # 3. LISTA DE RESERVAS
    path('clientes/reservas/', views.lista_reservas_clientes, name='lista_reservas_clientes'),
    
    # 4. CANCELAR RESERVA (Acción POST)
    path('clientes/reservas/cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]