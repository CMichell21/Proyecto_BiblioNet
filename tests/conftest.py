import pytest
from django.apps import apps

# LISTA DE APLICACIONES CON managed=False
# Incluye todas las aplicaciones que tienen modelos que deben ser creados
# en la base de datos de Pytest (seguridad y biblio).
# Si tienes más aplicaciones con managed=False, añádelas aquí.
APPS_TO_FORCE_MANAGE = ['seguridad', 'biblio'] 

@pytest.fixture(scope="session", autouse=True)
def setup_unmanaged_models_for_tests():
    """
    Este fixture anula temporalmente 'managed=False' en los modelos listados.
    Fuerza a Pytest a crear las tablas necesarias (roles, usuarios, etc.) 
    en la base de datos de pruebas temporal para evitar el 'no such table'.
    """
    
    # Almacena el estado original (aunque en el entorno de pruebas es efímero)
    original_managed_states = {}

    # Fase de Preparación (Modificación de Modelos en Memoria)
    for app_name in APPS_TO_FORCE_MANAGE:
        try:
            app_config = apps.get_app_config(app_name)
            for model in app_config.get_models():
                # Solo modificamos si realmente es managed=False
                if not model._meta.managed:
                    original_managed_states[model._meta.label] = model._meta.managed
                    # ¡El cambio clave! Fuerza a Django a gestionar este modelo para la prueba.
                    model._meta.managed = True
        except LookupError:
            # Continúa si la aplicación no está instalada
            continue 

    # Permite que las pruebas se ejecuten (incluyendo la creación de la DB)
    yield

    # Fase de Limpieza (Restauración del Estado Original)
    for app_name in APPS_TO_FORCE_MANAGE:
        try:
            app_config = apps.get_app_config(app_name)
            for model in app_config.get_models():
                if model._meta.label in original_managed_states:
                    model._meta.managed = original_managed_states[model._meta.label]
        except LookupError:
            continue
        